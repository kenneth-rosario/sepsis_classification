from keras.datasets import imdb
from keras.preprocessing import sequence
import numpy as np


def generateData():

    #Here we generate data that reflects our potential dataset
    #Strucutre is like this:
    #We have a total of 200000 patients for out training dataset
    #Each patient has a matrix of shape (15,48)
    #This means that each patient has data from hour 1 to hour 15
    #For every hour, we have 48 feautures which could be pulse, breathing rate, etc

    #Here we create our parameters
    train_patients = 100000
    test_patients = 20000
    hours = 12
    features_per_hour = 24

    #Here we create a random set of 100000 patient with high number value for every feature
    #This would represent our patients with sepsis
    x_sepsis = np.random.random((train_patients,hours,features_per_hour)) * 10000
    #Here we create another 100000 patients but with numbers ranging from 0 to 1
    #which is very low compared to the other patients. This patients don't have sepsis
    x_not_sepsis = np.random.random((train_patients,hours,features_per_hour))
    #Here we join both list of patients to form our 200000 patients dataset
    x_train = np.append(x_sepsis, x_not_sepsis, axis=0)

    #Here we just create a list of 1s for the first 100000 patients which correlate
    #with the patients with high numbers features. 
    y = np.ones((train_patients,1))
    #Here we create a list of zeros which belong to our patients without sepsis
    y2 = np.zeros((train_patients,1))
    #Now we join both lists
    y_train = np.append(y, y2, axis=0)

    #Since both X and Y are in order, we shuffle them here
    randomize = np.arange(len(y_train))
    np.random.shuffle(randomize)
    x_train = x_train[randomize]
    y_train = y_train[randomize]


    #We repeat the exact same process as above, but here we create fewer patients
    #This other dataset is to validate the data of our network.
    x_sepsis = np.random.random((test_patients,hours,features_per_hour)) * 10000
    x_not_sepsis = np.random.random((test_patients,hours,features_per_hour))
    x_test = np.append(x_sepsis, x_not_sepsis, axis=0)

    y = np.ones((test_patients,1))
    y2 = np.zeros((test_patients,1))
    y_test = np.append(y, y2, axis=0)

    randomize = np.arange(len(y_test))
    np.random.shuffle(randomize)
    x_test = x_test[randomize]
    y_test = y_test[randomize]

    #Here we return 2 tuples with our generated data
    return (x_train, y_train), (x_test, y_test)
