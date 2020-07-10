import argparse
import sys
import os
import random
import spotipy
import spotipy.util as util

# constants
SCOPE = 'user-library-read playlist-modify-private playlist-modify-public'
CLIENT_ID='f28ebd5ea47c46e2a4a6fc886bccc5f8'
REDIRECT_URI='http://localhost:8888/callback/'

parser = argparse.ArgumentParser(description='Makes a random playlist')
parser.add_argument('client_secret', type=str)
parser.add_argument('username', type=str)
parser.add_argument('num_songs', type=int)
parser.add_argument('playlist_name', type=str)

args = parser.parse_args()

client_secret = args.client_secret
username = args.username
num_songs = args.num_songs
playlist_name = args.playlist_name

# TODO get rid of these by sending multiple requests at the end
if num_songs>100 or num_songs<1:
    sys.exit('The number of songs must be between 1 and 100')

if not os.path.exists('.cache-' + username):
    print('A webpage will be launched, it will probably say not found, just copy and paste the link into the terminal'  )

token = util.prompt_for_user_token(username, SCOPE,CLIENT_ID,client_secret,REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    sys.exit('Bad token')


# TODO cache this
track_ids=[]

# TODO create playlist lazily
# TODO (w/ confirmation) overwrite existing playlist if exists
sp.user_playlist_create(username,playlist_name,public=True,description='made with makeRandomPlaylist')
playlists = sp.user_playlists(username)['items']
id=''
for i in range(len(playlists)):
    if playlists[i]['name']==playlist_name:
        id=playlists[i]['uri']
if not id:
    sys.exit('unable to find uri for playlist')


#get user saved tracks, spotify api only lets you get 50 songs per query, so have to repeateadly query
print('getting your saved tracks(this may take a few minutes)')
os=0
# TODO optional limit for how many tracks to download for faster development
while os<9999:
    # TODO pull out limit as constant and make optional arg
    results = sp.current_user_saved_tracks(limit=50,offset=os)
    for item in results['items']:
        track = item['track']
        track_ids.append(track['uri'])

    os=os+50
    prog='\r' + str(format(os/10000*100,'.2f'))+'%'
    #prog=str(format(os/10000*100))
    sys.stdout.write( prog )
    sys.stdout.flush()


rand=random.sample(range(len(track_ids)),num_songs)
out_tracks=[]
for i in rand:
    out_tracks.append(track_ids[i])
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    sp.user_playlist_add_tracks(username, id, out_tracks)

print('\n',num_songs, ' songs added to ', playlist_name)
