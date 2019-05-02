import numpy as np
import pickle
from sklearn.model_selection import train_test_split

def getDataset():
    with open("dataset/sepsis-patients-V1.pickle", "rb") as f:
        sepsis = []
        for stay in pickle.load(f):
            if len(stay) >= 50:
                sepsis.append(stay[:50][:])
        sepsis = np.array(sepsis)
        print(sepsis.shape)
        y_sepsis = np.zeros((len(sepsis),))


    with open("dataset/non-sepsis-patients-V1.pickle", "rb") as f:
        non_sepsis = []
        for stay in pickle.load(f):
            if len(stay) >= 50:
                non_sepsis.append(stay[:50][:])
            
            if len(non_sepsis) == 10000:
                break
        non_sepsis = np.array(non_sepsis)
        y_non_sepsis = np.ones((len(non_sepsis),))

    x_train1, x_val1, y_train1, y_val1 = train_test_split(sepsis, y_sepsis, test_size=0.30)
    x_val1, x_test1, y_val1, y_test1 = train_test_split(x_val1, y_val1, test_size=0.33) 


    x_train2, x_val2, y_train2, y_val2 = train_test_split(non_sepsis, y_non_sepsis, test_size=0.30)
    x_val2, x_test2, y_val2, y_test2 = train_test_split(x_val2, y_val2, test_size=0.33) 

    x_train = np.append(x_train1, x_train2, axis=0)
    x_val = np.append(x_val1, x_val2, axis=0)
    x_test = np.append(x_test1, x_test2, axis=0)
    y_train = np.append(y_train1, y_train2, axis=0)
    y_val = np.append(y_val1, y_val2, axis=0)
    y_test = np.append(y_test1, y_test2, axis=0)

    randomize = np.arange(len(y_train))
    np.random.shuffle(randomize)
    x_train = x_train[randomize]
    y_train = y_train[randomize]

    randomize = np.arange(len(y_val))
    np.random.shuffle(randomize)
    x_val = x_val[randomize]
    y_val = y_val[randomize]

    randomize = np.arange(len(y_test))
    np.random.shuffle(randomize)
    x_test = x_test[randomize]
    y_test = y_test[randomize]

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)