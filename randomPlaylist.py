import sys
import numpy
import spotipy
import spotipy.util as util
scope = 'user-library-read playlist-modify-private playlist-modify-public'
client_id='1c4e52b850ef400c985c051b42af8e94'
client_secret='7094d54d0a434c57a0402741ffa1e03b'
redirect_uri='http://localhost:8888/callback/'
# check arguments
if len(sys.argv) > 2:
    username = sys.argv[1]
    num_songs=int(sys.argv[2])
else:
    sys.exit('Bad Arguments')

if num_songs>100 or num_songs<1:
    sys.exit('The number of songs must be between 1 and 100')
# get and check token
print('Your browser will probably say the site can be reached, just copy and paste the url into the terminal. '  )
token = util.prompt_for_user_token(username, scope,client_id,client_secret,redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    sys.exit('Bad token')    
    
 
track_ids=[]

playlists = sp.user_playlists(username)
first=playlists['items'][0]
targ_playlist=first['uri']


# get user saved tracks, spotify api only lets you get 50 songs per query, so have to repeateadly query
print('getting your saved tracks(this may take a few minutes)')
os=0
while os<9999:
    results = sp.current_user_saved_tracks(limit=50,offset=os)
    for item in results['items']:
        track = item['track']
        track_ids.append(track['uri'])
   
    os=os+50   
    prog='\r' + str(format(os/10000*100,'.2f'))+'%'
    #prog=str(format(os/10000*100))
    sys.stdout.write( prog )
    sys.stdout.flush()


rand=numpy.random.choice(a=range(len(track_ids)),size=num_songs, replace=False)
out_tracks=[]
for i in rand:
    out_tracks.append(track_ids[i])
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    sp.user_playlist_add_tracks(username, targ_playlist, out_tracks)

print('\n',num_songs, ' songs added to ', first['name'])


    

