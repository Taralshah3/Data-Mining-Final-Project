import spotipy, json, os, csv
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id='1224d9e8587b44b4bb028a60ff591da9', client_secret='513772d259cc4813862ddbbb77c25645', redirect_uri='http://localhost:8080'))

playlist_ids = []

# Retrieve songs and basic song bio info from the API
categories = sp.categories(limit=50)['categories']['items']
print("Identifying playlists...")
for c in categories:
    playlists = []
    try:
        playlists = sp.category_playlists(category_id=c['id'], limit=50)['playlists']['items']
    except spotipy.exceptions.SpotifyException:
        print("   - Category for " + c['id'] + " doesn't exist.")
    if (playlists):
        for p in playlists:
            playlist_ids.append(p['id'])
print("... Gottem.")

songs = []

# Retrieve songs and basic song bio info from the API
print("Fetching playlist songs...")
for i in playlist_ids:
    s = sp.playlist(i, additional_types=("track",))['tracks']['items']
    songs = songs + s
print("... Gottem.")

track_ids = []
id_to_details = {}

# Save the data we want to maybe use in classification,
# add the track ID to track_ids for use in fetching audio features
for song in songs:
    if 'track' in song and song['track'] is not None:
        if 'id' in song['track'] and 'name' in song['track'] and 'popularity' in song['track']:
            track_ids.append(song['track']['id'])
            id_to_details[song['track']['id']] = {
                'name': song['track']['name'],
                'popularity': song['track']['popularity']
            }

print("Fetching audio features...")
# Retrieve the fun song data like danceability, energy, tempo, etc.
done = False
i = 0
l = len(track_ids)
while not done:
    id_subset = track_ids[(i * 100):((i + 1) * 100)]
    if ((i + 1) * 100 > l):
        done = True
    else:
        i += 1
    audio_features = sp.audio_features(tracks=id_subset)
    for af in audio_features:
        if af and 'id' in af:
            id_to_details[af['id']].update(af)
print("... Gottem.")

path = os.getcwd() + "\\Proj"

f = open(path + "\\all_song_data.json", "w")
f.write(json.dumps(id_to_details))
f.close()

with open(path + "\\AllSongData.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['song name','danceability (0-1)','energy (0-1)','valence (0-1)','tempo (BPM)','loudness (Decibels)','speechiness (0-1)','instrumentalness (0-1)','How much we like it  (1-10)'])
    for song in id_to_details:
        s = id_to_details[song]
        writer.writerow([s['name'], s['danceability'], s['energy'], s['valence'], s['tempo'], s['loudness'], s['speechiness'], s['instrumentalness']])