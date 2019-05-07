import pickle

# script to create data set without stays that have less than 24 hours

def stays_reduction(filename = "sepsis-patients-V1.pickle"):

    with open(filename, 'rb') as pickle_file, open("sepsis-patients-V4.pickle", 'wb') as pickle_out:

        allStaysV4 = []
        data_set = pickle.load(pickle_file)
        numberOfPatientsRemoved =0

        for stay in data_set:
            if len(stay) >= 24:
                allStaysV4.append(stay)

            else:
                #skip current stay
                numberOfPatientsRemoved=+1

        print("Number of patients removed: " + str(numberOfPatientsRemoved))
        print("Number of patients in new file: " + str(len(allStaysV4)))

        pickle.dump(allStaysV4, pickle_out)

if __name__ == '__main__':
    stays_reduction()
