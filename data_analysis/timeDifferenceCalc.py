from csv_extract import csv_generator
import time
import json

def calcTimeDiff():
    print("Calculating Time Diffs")

    timeRow = 3
    stayIdRow = 2

    lastTime = 0
    currentTime = 0

    timeDiffs = []
    currentID = 0
    allTimeDiffs = []

    for counter, row in enumerate(csv_generator(), start=0):
        if counter > 1:
            currentTime = time.mktime(time.strptime(row[timeRow], '%Y-%m-%d %H:%M:%S'))
           
            #We're still looking at the same stay
            if currentID == row[stayIdRow]:
                currentTimeDiff = currentTime - lastTime 
                timeDiffs.append(currentTimeDiff)
                    
            else:
                #We just found a new id
                patientStay = {"id": currentID, "TimeDiffs": timeDiffs, "Total": sum(timeDiffs) }
                allTimeDiffs.append(patientStay)

                timeDiffs = []
                currentID = row[stayIdRow]

            lastTime = currentTime

        elif counter == 1:
            lastTime = time.mktime(time.strptime(row[timeRow], '%Y-%m-%d %H:%M:%S'))
            currentID = row[stayIdRow]

    
    patientStay = {"id": currentID, "TimeDiffs": timeDiffs, "Total": sum(timeDiffs)}
    allTimeDiffs.append(patientStay)

    with open("allTimeDiffs.json", "w") as f:
        json.dump(allTimeDiffs, f, indent=4)

    print("Data saved: allTimeDiffs.json")

    total = []
    for stay in allTimeDiffs:
        total.append(stay["Total"])
    
    print("Average time span per patient:", sum(total) / len(total))
    print("Minimum time span per patient:", sorted(set(total))[1])
    print("Maximum time span per patient:", max(total))
    

def calcTimeDiffMinMax():
    print("Calculating Min and Max Time Diffs")

    allTimeDiffs = [] 
    allTimeDiffMinMax = []
    
    with open("allTimeDiffs.json") as f:
        allTimeDiffs = json.load(f)

    for stay in allTimeDiffs:
        if len(stay["TimeDiffs"]) > 1:
            #Removes all duplicate entries
            uniqueTimeDiffs = set(stay["TimeDiffs"])

            if len(uniqueTimeDiffs) > 1:
                #Sort unique set in ascending order
                minTimeDiff = sorted(uniqueTimeDiffs)[1]
            else:
                minTimeDiff = 0.0

            #Get the max number from the current
            maxTimeDiff = max(uniqueTimeDiffs)

            patientStay = {"id": stay["id"], "Min": minTimeDiff, "Max": maxTimeDiff}
            allTimeDiffMinMax.append(patientStay)
        else:
            print("Stay with ID", stay["id"], "doesn't have enough TimeDiff data:", stay["TimeDiffs"])

    with open("allTimeDiffMinMax.json", "w") as f:
        json.dump(allTimeDiffMinMax, f, indent=4)

    print("Data saved: allTimeDiffMinMax.json")

def countZerosTimeDiffs():
    print("Counting Zero Time Diffs")

    allTimeDiffs = [] 
    allZeroCounts = []
    
    with open("allTimeDiffs.json") as f:
        allTimeDiffs = json.load(f)

    for stay in allTimeDiffs:
        if len(stay["TimeDiffs"]) > 0:
            zeroCount = 0
            totalTimeDiffs = 0

            for timeDiff in stay["TimeDiffs"]:
                totalTimeDiffs += 1
                if timeDiff == 0.0:
                    zeroCount += 1

            patientStay = {"id": stay["id"], "Zeros": zeroCount, "Total": totalTimeDiffs, "Avg": zeroCount / totalTimeDiffs}
            allZeroCounts.append(patientStay)

    with open("allZeroCounts.json", "w") as f:
        json.dump(allZeroCounts, f, indent=4)

    print("Data saved: allZeroCounts.json")

def calcMinMaxTimeDiffAvg():
    print("Calculating Average Min and Max Time Diffs")

    allTimeDiffMinMax = []
    totalMinTimeDiffs = 0
    totalMaxTimeDiffs = 0
    totalTimeDiffs = 0

    with open("allTimeDiffMinMax.json") as f:
        allTimeDiffMinMax = json.load(f)


    for stay in allTimeDiffMinMax:
        totalTimeDiffs += 1
        totalMinTimeDiffs += stay["Min"]
        totalMaxTimeDiffs += stay["Max"]

    print("Average Minimum Time Difference:", totalMinTimeDiffs / totalTimeDiffs, "seconds")
    print("Average Maximum Time Difference:", totalMaxTimeDiffs / totalTimeDiffs, "seconds")

def calcZeroTimeDiffAvg():
    print("Calculating Average Zero Time Diffs")

    allZeroCounts = []
    totalZeroTimeDiffs = 0
    totalTimeDiffs = 0

    with open("allZeroCounts.json") as f:
        allZeroCounts = json.load(f)

    for stay in allZeroCounts:
        totalTimeDiffs += 1
        totalZeroTimeDiffs += stay["Zeros"]

    print("Average Zero Time Difference Count Per Stay:", totalZeroTimeDiffs / totalTimeDiffs)

if __name__ == "__main__":
    print("Calculating Time Diffs Data")
    print("This takes a lot of time")
    print("Sit back and relax\n\n")
    calcTimeDiff()
    calcTimeDiffMinMax()
    countZerosTimeDiffs()
    calcMinMaxTimeDiffAvg()
    calcZeroTimeDiffAvg()
    print("DONE!!!")
