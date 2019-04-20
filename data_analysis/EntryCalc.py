from csv_extract import csv_generator
import json

def rowsPerStay():
    print("Checking entries per stay..")
    stayIdColumn = 2
    currentID = 0
    currentEntries=0
    allEntries = []

    for counter, row in enumerate(csv_generator(), start=0):
        if counter==0:
            currentID=row[stayIdColumn]

        if currentID == row[stayIdColumn]:
            currentEntries+=1
                    
        else:
            patientStay = {"id": currentID, "featureEntries": currentEntries}
            allEntries.append(patientStay)
            currentID = row[stayIdColumn]
            #Starting on 1 since this entry is ignored on next iteration
            currentEntries=1

    with open("totalEntries.json", "w") as f:
        json.dump(allEntries, f, indent=4)

    print("Finished counting entries per stay.")

def entryAverage():
    print("Calculating average amount of entries per stay.")
    
    with open("totalEntries.json") as entries:
        allEntries = json.load(entries)

    entryAmount=0
    for patient in allEntries:
        entryAmount+=patient["featureEntries"]
    avgEntries=entryAmount/len(allEntries)

    print("Finished, average entries per patient:",avgEntries)

if __name__ == "__main__":
    rowsPerStay()
    entryAverage()
    print("Done.")
