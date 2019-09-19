import sys
import os
import numpy
import spotipy
import spotipy.util as util
scope = 'user-library-read playlist-modify-private playlist-modify-public'
client_id='1c4e52b850ef400c985c051b42af8e94'
client_secret=sys.argv[1]
redirect_uri='http://localhost:8888/callback/'
# check arguments
if len(sys.argv) > 3:
    username = sys.argv[2]
    num_songs=int(sys.argv[3])
    plname=sys.argv[4]
else:
    sys.exit('Bad Arguments')

if num_songs>100 or num_songs<1:
    sys.exit('The number of songs must be between 1 and 100')
if not os.path.exists('.cache-' + username):
    print('A webpage will be launched, it will probably say not found, just copy and paste the link into the terminal'  )
token = util.prompt_for_user_token(username, scope,client_id,client_secret,redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    sys.exit('Bad token')


track_ids=[]

sp.user_playlist_create(username,plname,public=True) #,description='made with makeRandomPlaylist  https://github.com/vinay-swamy/makeRandomPlaylistSpotify/')
playlists = sp.user_playlists(username)['items']
id=''
for i in range(len(playlists)):
    if playlists[i]['name']==plname:
        id=playlists[i]['uri']
if not id:
    sys.exit('unable to find uri for playlist')


#get user saved tracks, spotify api only lets you get 50 songs per query, so have to repeateadly query
print('getting your saved tracks(this may take a few minutes)')
os=0
art2song={}
total=sp.current_user_saved_tracks(limit=50,offset=os)['total'] + 10
# a little hacky but it works
while os<total:
    results = sp.current_user_saved_tracks(limit=50,offset=os)
    for item in results['items']:
        track = item['track']
        artist=track['artists'][0]['name']
        if artist in art2song:
            art2song[artist].append(track['uri'])
        else:
            art2song[artist]=[track['uri']]
    os=os+50
    prog='\r' + str(format(os/total*100,'.2f'))+'%'
    #prog=str(format(os/10000*100))
    sys.stdout.write( prog )
    sys.stdout.flush()
#print(art2song['Faded Paper Figures'])
#
#
k=list(art2song.keys())
rand=numpy.random.choice(a=range(len(k)),size=num_songs, replace=False)
out_tracks=[]
for i in rand:
    l=art2song[k[i]]
    j=numpy.random.choice(a=range(len(l)),size=1, replace=False)[0]
    out_tracks.append(l[j])
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    sp.user_playlist_add_tracks(username, id, out_tracks)

print('\n',num_songs, ' songs added to ', plname)
