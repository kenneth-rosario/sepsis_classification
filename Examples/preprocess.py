from keras.datasets import imdb
from keras.preprocessing import sequence
import numpy as np


def generateData():

    #Here we are loading a dataset from IMDB
    #Here we specify that for every sample, we want a max of 128 words
    #The max number of unique words should be 500
    #Words here are represented with their unique number
    #It doesn't matter to us this number to word relation
    max_features = 500
    max_len = 128
    print('Loading data...')

    #Here we call the imdb dataset and obtain teh data
    #Data is split into Trainin and Testing datasets
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

    print("X_test shape before padding:", x_test.shape)

    #We apply padding to chage X's dimension 
    x_train = sequence.pad_sequences(x_train, maxlen=max_len)
    x_test = sequence.pad_sequences(x_test, maxlen=max_len)

    print('X_test shape after padding:', x_test.shape)
    print("Y_test shape:", y_test.shape)

    #Here we are printing the value of the first sample
    print("Value of first sample ->", x_test[0])
    #Here we print the value of the first sample's last element
    print("Value of first sample's last value ->", x_test[0,-1])

    #Here we return 2 tuples each containing their X and Y matrices
    return (x_train, y_train), (x_test, y_test)


if __name__ == '__main__':
    generateData()