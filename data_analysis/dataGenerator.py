import time
import pickle
from csv_extract import csv_generator

totalFeatures = 18

def initializeHour():
    return [-1] * totalFeatures

def getFeatureIndices():
    return {
        #"FIO2":0,
        #"FIO2 [Meas]":0,
        #"Bilirubin":0,
        #"Manual BP [Systolic]":0,
        #"Skin Temperature":0,
        #"Bilirubin_ApacheIV":0,
        #"Direct Bilirubin":0,
        "Arterial BP [Systolic]":0,
        "Arterial Blood Pressure systolic":0,
        "Arterial BP #2 [Systolic]":0,
        "Eye Opening":1,
        "GCS - Eye Opening":1,
        "FiO2 Set":2,
        "Heart Rate":3,
        "Motor Response":4,
        "GCS - Motor Response":4,
        "NBP [Systolic]":5,
        "Non Invasive Blood Pressure systolic":5,
        "PAO2":6, 
        "Arterial PaO2":6,
        "SpO2":7,
        "Temperature C":8,
        "Temperature F":8,
        "Temperature Fahrenheit":8,
        "Temperature Celsius":8,
        "Verbal Response":9,
        "GCS - Verbal Response":9,
        "Platelets":10,
        "Creatinine":11,
        "RV systolic pressure(PA Line)":12,
        "PA systolic pressure(PA Line)":13,
        "Total Bilirubin":14,
        "Respiratory Rate":15,
        "Inspired O2 Fraction":16,
        "Skin Temperature":17
    }


def fixValues(feature, value, stringValue):
    if value != "":
        if "temperature" in feature.lower() and "skin" not in feature:
            value = float(value)
            if "C" in feature:
                return value + 273.15

            if "F" in feature:
                return (value - 32.0) * (5.0/9.0) + 273.15

    if "skin" in feature.lower():
        if "cool" in stringValue.lower():
            return 1.0

        if "warm" in stringValue.lower():
            return 2.0

        if "hot" in stringValue.lower():
            return 3.0

    return value


def addFeature(feature, value, hour, stringValue, stayID):
    value = fixValues(feature, value, stringValue)

    if value != "":
        index = getFeatureIndices().get(feature)

        if index != None:
            if hour[index] != -1:
                #For now just set mean
                #We will be using standard deviation to determine
                #That mean falls between a "real" range in the future
                hour[index] = (hour[index] + value) / 2.0
            
            else:
                hour[index] = value

    else:
        print("Stay", stayID, "has an empty string value for", feature)  

def saveData():
    print("Creating Dataset with feature extraction per hour")
    
    featureColumn = 0
    stayIdColumn = 2
    timeColumn = 3
    stringValueColumn = 4
    valueColumn = 5

    #LastTime is only updated when we pass the one hour mark
    lastTime = 0
    currentTime = 0
    currentID = 0
    day = 86400
    hour = 3600

    currentHour = []
    currentStay = []
    allStays = []

    #Used for knowing if we need to append last hour
    addLastHour = False


    for counter, row in enumerate(csv_generator(), start=0):
        if counter > 1:
            currentTime = time.mktime(time.strptime(row[timeColumn], '%Y-%m-%d %H:%M:%S'))

            if currentID == row[stayIdColumn]:
                
                if currentTime - lastTime <= hour:
                    addFeature(row[featureColumn], row[valueColumn], currentHour, row[stringValueColumn], row[stayIdColumn])
                    addLastHour = True
                
                else:
                    lastTime = currentTime
                    currentStay.append(currentHour)
                    currentHour = initializeHour()
                    addFeature(row[featureColumn], row[valueColumn], currentHour, row[stringValueColumn], row[stayIdColumn])
                    addLastHour = False
            else:
                #We have switched to a new stay
                lastTime = currentTime
                currentStay.append(currentHour)
                allStays.append(currentStay)
                currentHour = initializeHour()
                addFeature(row[featureColumn], row[valueColumn], currentHour, row[stringValueColumn], row[stayIdColumn])
                #Uneccasary to add, but you never know
                addLastHour = False


        elif counter == 1:
            lastTime = time.mktime(time.strptime(row[timeColumn], '%Y-%m-%d %H:%M:%S'))
            currentStay = []
            currentHour = initializeHour()
            addFeature(row[featureColumn], row[valueColumn], currentHour, row[stringValueColumn], row[stayIdColumn])

    #We have exited for loop. However, we still need to append the last hour to the last patient
    if addLastHour:
        currentStay.append(currentHour)
        allStays.append(currentStay)

    with open("datasetV1.pickle", "wb") as f:
        pickle.dump(allStays, f)

    print("Data saved: datasetV1.pickle")


if __name__ == "__main__":
    saveData()
