import pandas as pd
import numpy as np
from lin_reg_spotify_final import *

def user_interface():
    #reads in playlist data
    df_playlist = pd.read_csv('JakesSongRatings.csv')
    playlist_data = df_playlist.to_numpy()

    #formats playlist data
    formatted_data, song_scores, unnormalized_data = load_data(playlist_data)

    #gets weights for linear regression
    weights = batch_gradient_descent(formatted_data,song_scores)

    #gets the ten best reccomendations
    reccomendations = assign_scores('SongData_large.csv',weights,unnormalized_data)

    #shows the user interface
    print("Hi! Your song reccomendations are:")
    num = 1
    for i in reccomendations:
        print(num, i)
        num+=1
    

user_interface()