import pickle
from saveDataset import getFeatureIndices

def exclude_patients_v3(filename = "sepsis-patients-V1.pickle"):

    with open(filename, 'rb') as pickle_file, open("sepsis-patients-V3.pickle", 'wb') as pickle_out:
        feature_dict = getFeatureIndices()
        v3_dataset = []
        data_set = pickle.load(pickle_file)
        number_of_patients_removed = 0
        # Fills frequency array with n 0 where n is the size of the feature vector
        frequency_list = [0 for i in data_set[0][0] ]

        for i in data_set:
            last_hour = i[-1]
            if last_hour[feature_dict["Eye Opening"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Arterial BP [Systolic]"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["FiO2 Set"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Heart Rate"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Motor Response"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["NBP [Systolic]"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Temperature C"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Verbal Response"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Creatinine"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["Platelets"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["PAO2"]] == -1:
                number_of_patients_removed += 1
            elif last_hour[feature_dict["SpO2"]] == -1:
                number_of_patients_removed += 1
            else:
                v3_dataset.append(i)
        
        for i in v3_dataset:
            for j in range(len(i[-1])):
                if i[-1][j] == -1:
                    frequency_list[j] += 1
            
        
        print("Total Patients Removed in Version 3:", number_of_patients_removed)
        print("Total Patients in v3:", len(v3_dataset))
        print("Patients Without Feature:", frequency_list)
        print("Number of Patients without this measurement: ")
        for i in feature_dict.keys():
            print(i,":", frequency_list[feature_dict[i]])

        pickle.dump(v3_dataset, pickle_out)

if __name__ == '__main__':
    exclude_patients_v3()
