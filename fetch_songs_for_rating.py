import spotipy, json, os, csv
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id='1224d9e8587b44b4bb028a60ff591da9', client_secret='513772d259cc4813862ddbbb77c25645', redirect_uri='http://localhost:8080'))

# The playlist ID of the target playlist can be found by right clicking the playlist
# and clicking "Share > Copy Spotify URI" at the bottom. This will give something like
# spotify:playlist:3MRmRaXmfEiYsd3E3yhVYX -- the end bit is the playlist ID used by the API
#04aX9H91OhJjYvFRoZ9PjT
#684StvTCFs1jQTfLGeTYHE
playlist_id = "684StvTCFs1jQTfLGeTYHE"
# Whether to append to the JSON file or overwrite it
append = False

# Retrieve songs and basic song bio info from the API
songs = sp.playlist(playlist_id, additional_types=("track",))['tracks']['items']

track_ids = []
id_to_details = {}

# Save the data we want to maybe use in classification,
# add the track ID to track_ids for use in fetching audio features
i = 0
exid = ""
for song in songs:
    if i == 0:
        i = 1
        exid = song['track']['id']
    track_ids.append(song['track']['id'])
    id_to_details[song['track']['id']] = {
        'name': song['track']['name'],
        'artist': song['track']['artists'][0]['name'],
        'release_year': song['track']['album']['release_date'][:4],
        'popularity': song['track']['popularity'],
        'track_no': song['track']['track_number']
    }

# Retrieve the fun song data like danceability, energy, tempo, etc.
audio_features = sp.audio_features(tracks=track_ids[:100])
for af in audio_features:
    id_to_details[af['id']].update(af)

for i in id_to_details[exid]:
    print(str(i) + ": " + str(id_to_details[exid][i]))

# If append variable is True, add gathered songs to existing song_data.json file
# Obviously this can't be a simple file append, we have to read in the object from the file,
# merge the lists, stringify the JSON again, then write that to the file in order to maintain
# a valid JSON object.
path = os.getcwd() + ""
if append:
    f = open(path + "\\song_data.json", "r")
    contents = f.read()
    song_data = dict()
    if contents:
        song_data = json.loads(contents)
    f.close()
    f = open(path + "\\song_data.json", "w")
    song_data.update(id_to_details)
    f.write(json.dumps(song_data))
    f.close()
else:
    f = open(path + "\\song_data.json", "w")
    f.write(json.dumps(id_to_details))
    f.close()

with open(path + "\\SongDataRated.csv", 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['song name','danceability (0-1)','energy (0-1)','valence (0-1)','tempo (BPM)','loudness (Decibels)','speechiness (0-1)','instrumentalness (0-1)','How much we like it  (1-10)'])
    for song in id_to_details:
        s = id_to_details[song]
        writer.writerow([s['name'], s['danceability'], s['energy'], s['valence'], s['tempo'], s['loudness'], s['speechiness'], s['instrumentalness']])