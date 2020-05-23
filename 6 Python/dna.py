from sys import argv, exit
import csv


def main():

    if len(argv) != 3:
        print("Usage: dna.py strFile sequenceFile")
        exit(1)

    # str = short tandem repeats
    strData = getStrData(argv[1])
    sequence = getSequence(argv[2])

    # str's to search for
    strSequences = list(strData[0].keys())
    strSequences.remove('name')

    counts = getSeqCounts(sequence, strSequences)

    print(getWinner(strData, strSequences, counts))


# Load str profiles DB into memory
def getStrData(fileName):
    data = []
    with open(fileName, "r") as csv_file:
        for row in csv.DictReader(csv_file):
            data.append(row)

    return data


# Load target sequence into memory
def getSequence(fileName):
    with open(fileName, "r") as f:
        seq = f.read()

    return seq


# Get the counts for the strs in DB
def getSeqCounts(sequence, strSequences):
    result = {}
    for s in strSequences:
        result[s] = getRepeatCount(sequence, s)

    return result


# Find repeat count of a given str
def getRepeatCount(sequence, strSequence):
    highest = 0
    counter = 0

    strLength = len(strSequence)

    i = 0
    while i <= (len(sequence) - (strLength - 1)):
        if sequence[i:i+strLength] == strSequence:
            counter += 1
            # Jump to next group to check
            i += strLength
        else:
            if counter != 0:
                highest = max(highest, counter)
                # Reset as streak broken
                counter = 0
            i += 1

    return highest


# See if the str counts matches anyone in the DB
def getWinner(strData, strSequences, counts):
    winner = 'No match'

    for entry in strData:
        counter = 0
        for strSeq in strSequences:

            if int(entry[strSeq]) == counts[strSeq]:
                counter += 1
            else:
                # Skip to next entry as soon as there is a no match
                break

        if counter == len(strSequences):
            winner = entry['name']
            break

    return winner


main()
