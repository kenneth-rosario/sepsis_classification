import pickle

def analyzeSofaScores(filename):
    allStays = []
    SOFA = []
    qSOFA = []

    with open(filename, "rb") as f:
        allStays = pickle.load(f)

    for stay in allStays:
        prevSOFA = stay[0][-2]
        for count, hour in enumerate(stay, start=1):
            SOFA.append(hour[-2])
            qSOFA.append(hour[-1])

    print("Average SOFA:", sum(SOFA) / len(SOFA))
    print("Min SOFA:", min(SOFA))
    print("Max SOFA", max(SOFA))
    print("Average qSOFA:", sum(qSOFA) / len(qSOFA))
    print("Min qSOFA:", min(qSOFA))
    print("Max qSOFA", max(qSOFA))

def analyzeOnsetSepsisHour(filename):
    allStays = []
    hours = []

    with open(filename, "rb") as f:
        allStays = pickle.load(f)

    for stay in allStays:
        prevSOFA = stay[0][-2]
        for count, hour in enumerate(stay, start=1):
            if hour[-2] - prevSOFA > 2:
                hours.append(count)
                break

            prevSOFA = hour[-2]

    print("Average Hour of Sepsis:", sum(hours) / len(hours))
    print("Min Hour:", min(hours))
    print("Max Hour", max(hours))

if __name__ == "__main__":
    filename = "sepsis-patients-V1.pickle"
    analyzeSofaScores(filename)
    analyzeOnsetSepsisHour(filename)
    
    print("/////////////////////////")

    filename = "non-sepsis-patients-V1.pickle"
    analyzeSofaScores(filename)
    analyzeOnsetSepsisHour(filename)
