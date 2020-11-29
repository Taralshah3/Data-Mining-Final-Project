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
    reccomendations, urls = assign_scores('SongData_large.csv',weights,unnormalized_data)

    #shows the user interface
    print("Hi! Your song reccomendations are:")
    print("**************************************")
    num = 1
    for i in range(0,len(reccomendations)):
        print(num, reccomendations[i])
        print("URL: ",urls[i])
        num+=1
    print("**************************************")

    #computes one-fold cross validation (un-comment to see), takes a while to compute but it works
    #print("The cross validation error of the training set is", cross_validation_error(unnormalized_data,song_scores))

user_interface()