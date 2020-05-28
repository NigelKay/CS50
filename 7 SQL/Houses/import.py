import cs50
import csv
from sys import argv, exit


def main():

    if len(argv) != 2:
        print("Usage: import.py fileName")
        exit(1)

    fileName = argv[1]
    db = cs50.SQL("sqlite:///students.db")

    with open(fileName, "r") as data:
        reader = csv.DictReader(data)

        for row in reader:
            # Unpack tuple of split name
            (first, middle, last) = splitName(row["name"])
            house = row["house"]
            birth = row["birth"]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       first, middle, last, house, birth)


# Split the name on whitespace and return tuple
def splitName(name):
    nameParts = name.split()

    if len(nameParts) == 3:
        return [nameParts[0], nameParts[1], nameParts[2]]
    else:
        return [nameParts[0], None, nameParts[1]]


main()
