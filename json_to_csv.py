import json, csv, os

path = os.getcwd()

f = open(path + "\\all_song_data.json", "r")
song_data = json.loads(f.read())

with open(path + "\\AllSongData_fromjson.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['song name','uri','danceability (0-1)','energy (0-1)','valence (0-1)','tempo (BPM)','loudness (Decibels)','speechiness (0-1)','instrumentalness (0-1)','How much we like it  (1-10)'])
    for song in song_data:
        s = song_data[song]
        try:
            writer.writerow([s['name'], s['uri'], s['danceability'], s['energy'], s['valence'], s['tempo'], s['loudness'], s['speechiness'], s['instrumentalness']])
        except KeyError as e:
            print("KeyError: " + s['name'])