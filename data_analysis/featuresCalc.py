from csv_extract import csv_generator
import json
import copy
from prettytable import PrettyTable
import sys

def numPatients():
    #Number of patientIDs

    print("Checking total number of patients...")

    patientIdColumn = 2
    currentID = 0
    numPatients = 0

    for counter, r in enumerate(csv_generator(), start=0):
        if counter == 0:
            currentID = r[patientIdColumn]

        if currentID != r[patientIdColumn]:
            numPatients += 1

    print("The number of patients is:", numPatients)

    return numPatients

def listOfPatients():
    #Helper method. Create a list of dictionaries which are patients
    allPatients = []
    patientIdColumn = 2
    currentID = 0

    for counter, r in enumerate(csv_generator(), start=0):
        if counter == 0:
            currentID = r[patientIdColumn]

        if currentID != r[patientIdColumn]:
            dic = {"StayID":r[patientIdColumn]}
            allPatients.append(dic)

    print("list done")
    return allPatients

def featuresPerPatient():
    # number of entries per feature for every patient

    print("Checking number of entries per feauture...")

    features = getFeatureList()
    featuresColumn = 0
    patientIdColumn = 2
    valuesColumn = 5
    currentID = 0
    currentPatient = {}
    featuresPerPatient = {}

    for counter, r in enumerate(csv_generator(), start=0):
        if counter != 0:
            if counter == 1:
                currentID = r[patientIdColumn]
                currentPatient = {}
                for feature in features:
                    currentPatient[feature] = 0
                
            if currentID == r[patientIdColumn] and r[valuesColumn] != "":
                currentPatient[r[featuresColumn]] += 1
            
            else:
                featuresPerPatient[currentID] = currentPatient 
                currentID = r[patientIdColumn]
                currentPatient = {}
                for feature in features:
                    currentPatient[feature] = 0

    featuresPerPatient[currentID] = currentPatient 

    with open("featuresPerPatient.json", "w") as f:
        json.dump(featuresPerPatient, f, indent=4)

    print("Info saved featuresPerPatient.json" )


def getFeatureList():
    featureList = []
    featuresColumn = 0
    for counter, r in enumerate(csv_generator(), start=0):
        if r[featuresColumn] not in featureList and r[featuresColumn] != "label":
            featureList.append(r[featuresColumn])

    return featureList
    
def getFeatureAvgOccurences():
    featuresPerPatient = {}
    featuresList = {}
    totalPatients = 0

    for feature in getFeatureList():
        featuresList[feature] = {}
        featuresList[feature]["total"] = 0
        featuresList[feature]["occurences"] = 0
        featuresList[feature]["min"] = 9999999999999
        featuresList[feature]["max"] = 0
        

    with open("featuresPerPatient.json", "r") as f:
        featuresPerPatient = json.load(f)

    for patient, features in featuresPerPatient.items():
        totalPatients += 1
        for feature, value in features.items():
            featuresList[feature]["total"] += value
            if value > 0:
                featuresList[feature]["occurences"] += 1

                if featuresList[feature]["min"] > value:
                    featuresList[feature]["min"] = value
                
                if featuresList[feature]["max"] < value:
                    featuresList[feature]["max"] = value

    t = PrettyTable(['Feature', 'Occurences', 'Average', 'Min', 'Max'])

    print("Total numer of stays", totalPatients)
    for feature, value in featuresList.items():
        if value["occurences"] == 0.0:
            avg = 0.0
        else:
            avg = value["total"] / value["occurences"]
        t.add_row([feature, value["occurences"], avg, value["min"], value["max"]])      

    print(t)


def featureValuesPerPatient():
    # number of entries per feature for every patient

    print("Checking values of entries per feauture...")

    features = getFeatureList()
    featuresColumn = 0
    valuesColumn = 5
    patientIdColumn = 2
    currentID = 0
    currentPatient = {}
    featuresValuesPerPatient = {}

    for counter, r in enumerate(csv_generator(), start=0):
        if counter != 0:
            if counter == 1:
                currentID = r[patientIdColumn]
                currentPatient = {}
                for feature in features:
                    currentPatient[feature] = []
                
            if currentID == r[patientIdColumn] and r[valuesColumn] != "":
                currentPatient[r[featuresColumn]].append(float(r[valuesColumn]))
            
            else:
                featuresValuesPerPatient[currentID] = currentPatient 
                currentID = r[patientIdColumn]
                currentPatient = {}
                for feature in features:
                    currentPatient[feature] = []

    featuresValuesPerPatient[currentID] = currentPatient 

    with open("featuresValuesPerPatient.json", "w") as f:
        json.dump(featuresValuesPerPatient, f, indent=4)

    print("Info saved featuresValuesPerPatient.json" )

def getFeatureValuesAvgOccurences():
    featuresValuesPerPatient = {}
    featuresList = {}
    totalPatients = 0

    for feature in getFeatureList():
        featuresList[feature] = {}
        featuresList[feature]["total"] = 0
        featuresList[feature]["occurences"] = 0
        featuresList[feature]["min"] = sys.maxsize
        featuresList[feature]["max"] = 0
        
    try:
        with open("featuresValuesPerPatient.json", "r") as f:
            featuresValuesPerPatient = json.load(f)
        
    except:
        featureValuesPerPatient()
        with open("featuresValuesPerPatient.json", "r") as f:
            featuresValuesPerPatient = json.load(f)


    for patient, features in featuresValuesPerPatient.items():
        totalPatients += 1
        for feature, value in features.items():
            featuresList[feature]["total"] += sum(value)

            if sum(value) > 0:
                featuresList[feature]["occurences"] += 1

                if featuresList[feature]["min"] > sum(value):
                    featuresList[feature]["min"] = sum(value)
                
                if featuresList[feature]["max"] < sum(value):
                    featuresList[feature]["max"] = sum(value)

    t = PrettyTable(['Feature', 'Occurences', 'Val Average', 'Val Min', 'Val Max'])

    print("Total numer of stays", totalPatients)
    for feature, value in featuresList.items():
        if value["occurences"] == 0.0:
            avg = 0.0
        else:
            avg = value["total"] / value["occurences"]
        t.add_row([feature, value["occurences"], avg, value["min"], value["max"]])        

    print(t)


if __name__ == "__main__":
    getFeatureAvgOccurences()
    print('\n')
    getFeatureValuesAvgOccurences()

    print("Done")