from csv_extract import csv_generator
import json

def numPatients():
    #Number of patientIDs

    print("Checking number of patients...")

    patientIdColumn = 2
    currentID = 0
    numPatients = 0

    for counter, r in enumerate(csv_generator(), start=0):
        if counter == 0:
            currentID = r[patientIdColumn]

        if currentID != r[patientIdColumn]:
            numPatients += 1

    print("Finished counting patients. The number of patients is:" + str(numPatients))

#def featuresperpatient():
    # number of entries per feature for every patient


def listOfPatients():
    #Helper method. Create a list of dictionaries which are patients

    allPatients = []
    patientIdColumn = 2
    currentID = 0

    for counter, r in enumerate(csv_generator(), start=0):
        if counter == 0:
            currentID = r[patientIdColumn]

        if currentID != r[patientIdColumn]:
            dic = {"PatientID":r[patientIdColumn]}
            allPatients.append(dic)

    return allPatients


if __name__ == "__main__":
    numPatients()
    #featuresPerPatient()

    print("Done")