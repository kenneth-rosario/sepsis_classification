import time
import pickle
import copy
from csv_extract import csv_generator

#Used for adding values later in Data Imputation
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def getFeatureIndices():
    return {
        #"Bilirubin":0,
        #"Manual BP [Systolic]":0,
        #"Bilirubin_ApacheIV":0,
        #"Direct Bilirubin":0,
        "Arterial BP [Systolic]":0,
        "Arterial Blood Pressure systolic":0,
        "Arterial BP #2 [Systolic]":0,
        "Eye Opening":1,
        "GCS - Eye Opening":1,
        "FiO2 Set":2,
        "FIO2":2,
        "FIO2 [Meas]":2,
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

def sepsisPatientIds():
    IDs = []
    stayIdColumn = 2
    currentID = 0

    for count, row in enumerate(csv_generator(), start=0):
        if count > 1:
            if row[stayIdColumn] != currentID:
                IDs.append(row[stayIdColumn])
                currentID = row[stayIdColumn]

        if count == 1:
            IDs.append(row[stayIdColumn])
            currentID = row[stayIdColumn]

    return IDs

totalFeatures = max(getFeatureIndices().values()) + 1

def initializeHour():
    return [-1.0] * totalFeatures

def fixValues(feature, value, stringValue):
    if value != "":
        value = float(value)
        if "temperature" in feature.lower() and "skin" not in feature:
            value = float(value)
            if "C" in feature:
                return value + 273.15

            if "F" in feature:
                return (value - 32.0) * (5.0/9.0) + 273.15

    if "skin" in feature.lower():
        if "cold" in stringValue.lower():
            return 1.0

        if "cool" in stringValue.lower():
            return 2.0

        if "warm" in stringValue.lower():
            return 3.0

        if "hot" in stringValue.lower():
            return 4.0

    if "Platelets" == feature:
        if "<5" in stringValue:
            return 5.0

    if "Creatinine" == feature:
        if "<0.5" in stringValue or "<.5" in stringValue:
            return 0.5
        if "<0.4" in stringValue or "<.4" in stringValue:
            return 0.4
        if "<0.3" in stringValue or "<.3" in stringValue:
            return 0.3
        if "<0.2" in stringValue or "<.2" in stringValue:
            return 0.2
        if "<0.1" in stringValue or "<.1" in stringValue:
            return 0.1

    return value


def addFeature(hour, feature, value, stringValue, stayID):
    value = fixValues(feature, value, stringValue)

    if value != "":
        index = getFeatureIndices().get(feature)

        if index != None:
            if hour[index] != -1:
                #If we have a previous value, for now we juwst overwrite that old value
                #We can use Standard Devaition or Mean as other options
                hour[index] = value
            else:
                hour[index] = value

    else:
        if stringValue != "":
            print("Stay", stayID, "has an empty string value for", feature) 
            print("The string value of the feature:", stringValue)
        if feature == "Skin Temperature":
            print(stringValue)

def saveData(filename="sepsis-patients.csv", skipSepsisPatients=False):

    print("Creating Dataset with feature extraction per hour")
    
    featureColumn = 0
    stayIdColumn = 2
    timeColumn = 3
    stringValueColumn = 4
    valueColumn = 5

    if skipSepsisPatients:
        sepsisPatients = sepsisPatientIds()
    else:
        sepsisPatients = []

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

    #Used for skipping current ID
    skipCurrentId = False


    for counter, row in enumerate(csv_generator(filename), start=0):
        #Here we skip row 0 because its just header info

        if counter > 1:
            currentTime = time.mktime(time.strptime(row[timeColumn], '%Y-%m-%d %H:%M:%S'))

            if currentID == row[stayIdColumn]:
                
                if currentTime - lastTime <= hour:
                    if skipCurrentId == False:
                        addFeature(currentHour, row[featureColumn], row[valueColumn], row[stringValueColumn], row[stayIdColumn])
                        addLastHour = True
                
                else:
                    if skipCurrentId == False:
                        lastTime = currentTime
                        currentStay.append(currentHour)
                        currentHour = initializeHour()
                        addFeature(currentHour, row[featureColumn], row[valueColumn], row[stringValueColumn], row[stayIdColumn])
                        addLastHour = False
            else:
                #We have switched to a new stay
                if skipCurrentId == False:
                    currentStay.append(currentHour)
                    allStays.append(currentStay)
                    
                skipCurrentId = False
                lastTime = currentTime
                currentStay = []
                currentID = row[stayIdColumn]
                currentHour = initializeHour()

                if currentID not in sepsisPatients:
                    addFeature(currentHour, row[featureColumn], row[valueColumn], row[stringValueColumn], row[stayIdColumn])
                    #Uneccasary to add, but you never know
                    addLastHour = False
                else:
                    skipCurrentId = True

        elif counter == 1:
            currentID = row[stayIdColumn]
            lastTime = time.mktime(time.strptime(row[timeColumn], '%Y-%m-%d %H:%M:%S'))
            currentHour = initializeHour()
            if currentID not in sepsisPatients:
                addFeature(currentHour, row[featureColumn], row[valueColumn], row[stringValueColumn], row[stayIdColumn])
            else:
                skipCurrentId = True
    #We have exited for loop. However, we still need to append the last hour to the last patient
    if addLastHour:
        currentStay.append(currentHour)
        allStays.append(currentStay)

    with open(filename.split('.')[0] + "-V1.pickle", "wb") as f:
        pickle.dump(allStays, f)

    print("Data saved:", filename.split('.')[0] + "-V1.pickle")


def appendSofaScores(filename):
    allStays = []
    eyeResponse = getFeatureIndices().get("Eye Opening")
    motorResponse = getFeatureIndices().get("Motor Response")
    verbalResponse = getFeatureIndices().get("Verbal Response")
    PAO2 = getFeatureIndices().get("PAO2")
    FIO2 = getFeatureIndices().get("FIO2")
    Bilirubin = getFeatureIndices().get("Total Bilirubin")
    Creatinine = getFeatureIndices().get("Creatinine")
    Platelets = getFeatureIndices().get("Platelets")
    ArterialBloodPressure = getFeatureIndices().get("Arterial Blood Pressure systolic")
    Respiration = getFeatureIndices().get("Respiratory Rate")

    print("Loading data from file")
    with open(filename, "rb") as f:
        allStays = pickle.load(f)

    print("Calculating SOFA score for every hour for every patient")
    for stay in allStays:
        for hour in stay:
            SOFA = 0.0

            #Calculate Glascow first
            #WE assume that user is good if value not recorded... for now
            eye = 4
            verbal = 5
            motor = 6

            #We only set response values if numbers are within standard range
            if hour[eyeResponse] in [1,2,3,4]:
                eye = hour[eyeResponse]
            if hour[verbalResponse] in [1,2,3,4,5]:
                verbal = hour[verbalResponse]
            if hour[motorResponse] in [1,2,3,4,5,6]:
                motor = hour[motorResponse]

            #Some heavy value checking can be done to deal with no values found 
            #Like setting response value absed on values of present values
            GCS = eye + verbal + motor


            if GCS == 13 or GCS == 14:
                SOFA += 1
            elif GCS >= 10 and GCS <= 12:
                SOFA += 2
            elif GCS >= 6 and GCS <= 9:
                SOFA += 3
            else:
                SOFA += 4

            #Respiratory System
            #Assume patient is alright if data isn't present
            ratio = 400.0

            #Here we check wether the values are present and not zero
            if hour[PAO2] not in [-1.0, 0.0] and hour[FIO2] not in [-1.0, 0.0]:
                ratio = hour[PAO2] / hour[FIO2]
            
            if 300 <= ratio <= 400:
                SOFA += 1
            elif 200 <= ratio < 300:
                SOFA += 2
            elif 100 <= ratio < 200:
                SOFA += 3
            elif ratio < 100:
                SOFA += 4

            #Liver System
            #Again, assume user is good on no values found in hour
            density = 1.0

            if hour[Bilirubin] != -1.0:
                density = hour[Bilirubin]

            if 1.2 <= density <= 1.9:
                SOFA += 1
            elif 2.0 <= density <= 5.9:
                SOFA += 2
            elif 6.0 <= density <= 11.9:
                SOFA += 3
            elif density >= 12.0:
                SOFA += 4


            #Kidneys
            density2 = 0.0

            if hour[Creatinine] != -1.0:
                density2 = hour[Creatinine]

            if 1.2 <= density2 <= 1.9:
                SOFA += 1
            elif 2.0 <= density2 <= 3.4:
                SOFA += 2
            elif 3.5 <= density2 <= 4.9:
                SOFA += 3
            elif density2 >= 5.0:
                SOFA += 4

            #Coagulation
            platelets = 160.0

            if hour[Platelets] not in [-1.0, 0.0]:
                platelets = hour[Platelets]

            if 100 <= platelets < 150:
                SOFA += 1
            elif 50 <= platelets < 100:
                SOFA += 2
            elif 20 <= platelets < 50:
                SOFA += 3
            elif platelets < 20:
                SOFA += 4

            #Cardiovascular System
            #Info on vasopressors administered not present, thus we are limited in here
            #to only user arterial blood pressure
            MAP = 100

            if hour[ArterialBloodPressure] not in [-1.0, 0.0]:
                MAP = hour[ArterialBloodPressure]

            if MAP < 70:
                SOFA += 1
            
            #We finished with SOFA scoring :)
            #Now lets calculate Quick SOfa
            #Can be useful to calculate
            qSOFA = 0.0

            respiratoryRate = 20.0

            if hour[Respiration] not in [-1.0, 0.0]:
                respiratoryRate = hour[Respiration]

            if MAP <= 100:
                qSOFA += 1

            if respiratoryRate >= 22:
                qSOFA += 1

            if GCS <= 15:
                qSOFA += 1

            #Finihsed with qSOFA, now we append this values to the hour vector

            hour.append(SOFA)
            hour.append(qSOFA)

    with open(filename, "wb") as f:
        pickle.dump(allStays, f)
    
    print("Finished calculating SOFA scores :)")
    print("Data saved:", filename)


def runDataImputation(filename):
    allStays = []
    print("Loading data from file")
    with open(filename, "rb") as f:
        allStays = pickle.load(f)


    print("Running Data Imputation on all features per hour")
    for stay in allStays:
        before = []
        for hourNumber, hour in enumerate(stay, start=0):
            if hourNumber > 0:
                for index, value in enumerate(hour, start=0):
                    if before[index] != -1.0:
                        if value == -1.0:    
                            hour[index] = copy.deepcopy(before[index])
                        else:
                            #Since value is present, update before value to this value
                            before[index] = copy.deepcopy(hour[index])

            else:
                #If in row 1
                #Iterate through next values and store nextValues per feature in before afterwards
                for index, value in enumerate(hour, start=0):
                    if value == -1.0:
                        for nextHour in stay[hourNumber+1:]:
                            if nextHour[index] != -1.0:
                                hour[index] = copy.deepcopy(nextHour[index])
                                break
                
                before = copy.deepcopy(hour)

    with open(filename, "wb") as f:
        pickle.dump(allStays, f)

    print("Finished Data Imputation")
    print("Data saved:", filename)


if __name__ == "__main__":
    filename = "sepsis-patients.csv"
    saveData(filename)
    
    dataset = "sepsis-patients-V1.pickle"
    runDataImputation(dataset)
    appendSofaScores(dataset)

    # filename = "non-sepsis-patients.csv"
    # saveData(filename, True)
    # dataset = "non-sepsis-patients-V1.pickle"
    # runDataImputation(dataset)
    # appendSofaScores(dataset)