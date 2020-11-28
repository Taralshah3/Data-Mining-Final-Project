import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

learningRate = 0.01
plotArray = []

#double check that this is working properly
def normalize_data_points(data_to_be_normalized, training_data):
    num_rows,num_cols = data_to_be_normalized.shape

    for i in range(0,num_cols):
        current_mean_column = np.mean(training_data[:,i])
        current_sd_column = np.std(training_data[:,i], ddof = 1)
        for b in range(0,num_rows):
            data_to_be_normalized[b,i] = (data_to_be_normalized[b,i]-current_mean_column)/current_sd_column
    
    return data_to_be_normalized

def load_data(song_data):
     data = song_data
     song_names = data[:,0]
     song_scores = np.array([]) 
     #removes headers
     data = np.delete(data,0,axis = 0)

     #removes song_names from the data
     data = np.delete(data,0,axis = 1)
    
     #gets song scores 
     #may need to change 7 depending on if we add/remove columns
     song_scores = data[:,7]

     #removes how much we like the song
     #may need to change the 7 depending on if we add more columns or not

     data = np.delete(data,7,axis = 1)

     normalized_data = normalize_data_points(data,data)
     return normalized_data,song_scores,data
     #print(batch_gradient_descent(normalized_data,song_scores))
     #print(normalized_data)


def batch_gradient_descent(data, song_scores):
    #need to alter weights to be 8
    weights = [0,0,0,0,0,0,0,0]
    numberExamples = len(data)

    currentError = 10000
    previousError = 0
    while(round(currentError,4) != round(previousError,4)):   #iterates until it converges
        previousError = currentError
        currentError = 0
        for b in range(0,8): #loops through every predictor
            totalError = 0
            for i in range(0,numberExamples):
                    estimation = weights[0]+weights[1]*data[i,0]+weights[2]*data[i,1]+weights[3]*data[i,2]+weights[4]*data[i,3]+weights[5]*data[i,4]+weights[6]*data[i,5]+weights[7]*data[i,6]
                    actual = song_scores[i]
                    error = actual-estimation
                    if(b == 0):
                        xValue = 1
                    else:
                        xValue = data[i,b-1]
                    totalError += xValue*error
            weights[b] += learningRate*totalError
            currentError += totalError
        #used for plot graphing
        plotArray.append(currentError)
    return weights

def assign_scores(filename, weights, unnormalized_data):
    df = pd.read_csv(filename) #pandas automatically removes headers
    data = df.to_numpy()

    
    data = data[:,0:8] #removes NaN values at the end of the array
    
    song_names = data[:,0]

    #removes songs column and normalizes bc you can't normalize song strings
    normalized_data = normalize_data_points(np.delete(data,0,1),unnormalized_data)

    #adds song names back in
    data = np.concatenate((song_names.reshape(-1,1),normalized_data),axis=1)

    predictions = np.array([]) #stores prediction for each example  
    num_rows, num_cols = data.shape

    for i in range(0,num_rows):
        estimation = weights[0]+weights[1]*data[i,1]+weights[2]*data[i,2]+weights[3]*data[i,3]+weights[4]*data[i,4]+weights[5]*data[i,5]+weights[6]*data[i,6]+weights[7]*data[i,7] #estimate of how much we will like a song from 1-10
        predictions = np.append(predictions,estimation)
    
    predictions = predictions.reshape(-1,1) #changes predictions array to be vertical
    data = np.concatenate((data,predictions), axis = 1) #adds the current data to the predictions 
    sorted_data = data[np.argsort(data[:,num_cols])]  #sorts the array by predictions
   
    
    ten_predictions = np.array([]) #stores ten reccomendations for songs by name 
    for i in range(0,10):
        ten_predictions = np.append(ten_predictions,sorted_data[num_rows-1-i,0]) #did this because np.sort sorts by lowest --> highest

    return ten_predictions #prints reccomendations highest --> lowest
