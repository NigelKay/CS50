from cs50 import get_string
from sys import exit


def main():
    cardNumber = get_string("Number: ")
    digitCount = len(cardNumber)

    if digitCount not in [13, 14, 15, 16]:
        print("INVALID")
        exit(1)

    if not passesLuhnAlgorithm(cardNumber):
        print("INVALID")
        exit(1)

    if checkAmericanExpress(digitCount, int(cardNumber[:2])):
        print("AMEX")
        exit(0)

    elif checkMasterCard(digitCount, int(cardNumber[:2])):
        print("MASTERCARD")
        exit(0)

    elif checkVisa(digitCount, int(cardNumber[0])):
        print("VISA")
        exit(0)

    else:
        print("INVALID")


def passesLuhnAlgorithm(cardNumber):
    reversedNumber = cardNumber[::-1]
    total = 0
    doubledNumbers = []

    for i in range(len(reversedNumber)):
        if i % 2 == 0:
            total += int(reversedNumber[i])
        else:
            doubledNumbers.append(int(reversedNumber[i]) * 2)

    for num in doubledNumbers:
        if num > 9:
            # if over 9, first digit guarenteed to be 1
            total += (1 + num % 10)
        else:
            total += num

    return total % 10 == 0


def checkAmericanExpress(length, firstDigits):
    if length != 15:
        return False
    if firstDigits != 34 and firstDigits != 37:
        return False

    return True


def checkMasterCard(length, firstDigits):
    if length != 16:
        return False
    if firstDigits not in range(51, 56):
        return False

    return True


def checkVisa(length, firstDigit):
    if length != 13 and length != 16:
        return False
    if firstDigit != 4:
        return False

    return True


main()
