import cs50
from sys import argv, exit


def main():

    if len(argv) != 2:
        print("Usage: import.py houseName")
        exit(1)

    houseName = argv[1]
    db = cs50.SQL("sqlite:///students.db")

    students = db.execute("SELECT first, middle, last, birth FROM students WHERE house=? ORDER BY last, first", houseName)

    for student in students:

        name = getName(student)
        birth = student['birth']

        print(f"{name}, born {birth}")


# Get name format based on presence of middle name
def getName(student):

    if student['middle'] is None:
        return student['first'] + ' ' + student['last']
    else:
        return student['first'] + ' ' + student['middle'] + ' ' + student['last']


main()
