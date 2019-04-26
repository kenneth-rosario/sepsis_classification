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
    print("list done")
    return allPatients

def featuresPerPatient():
    # number of entries per feature for every patient

    print("Checking number of entries per feature...")

    list = listOfPatients()
    featuresColumn = 1
    patientIdColumn = 2
    currentID =0
    currentDic = 0
    currentPatient = list[currentDic]

    for counter, r in enumerate(csv_generator(), start=0):
        while counter < len(list):
            if counter == 0:
                currentID = r[patientIdColumn]

            if currentID != r[patientIdColumn]:
                currentDic += 1
                currentPatient = list[currentDic]

            if r[featuresColumn] in currentPatient:
                currentPatient[r[featuresColumn]] += 1
            else:
                currentPatient.update({r[featuresColumn]:1})

    with open("featuresPerPatient.json", "w") as f:
        json.dump(list, f, indent=4)

    print("Finished creating featuresPerPatient.json file." )


if __name__ == "__main__":
    numPatients()
    featuresPerPatient()

    print("Done")