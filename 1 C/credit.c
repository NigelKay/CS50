#include <cs50.h>
#include <stdio.h>

long getCardNumber();
int checkDigitLength(long input);
bool passesLuhnAlgorithm(long cardNumber, int length);
int calculateDoubledArrayTotal(int doubledArray[], int doubleDigitCount);
int getFirstDigits(long cardNumber);
bool checkAmericanExpress(int length, int firstDigits);
bool checkMasterCard(int length, int firstDigits);
bool checkVisa(int length, int firstDigits);

int main(void)
{
    long cardNumber = get_long("Number: ");
    int digitCount = checkDigitLength(cardNumber);
    // // Break early if invalid length
    if (digitCount < 13 || digitCount > 16) 
    {
        printf("INVALID\n");
        return (0);
    }
    
    // Break early if fails Luhns algorithm
    if (!passesLuhnAlgorithm(cardNumber, digitCount))
    {
        printf("INVALID\n");
        return (0);
    }
    
    // check each card instance or default to invalid
    int leadingDigits = getFirstDigits(cardNumber);
    if (checkAmericanExpress(digitCount, leadingDigits))
    {
        printf("AMEX\n");
        return (0);
    }
    else if (checkMasterCard(digitCount, leadingDigits))
    {
        printf("MASTERCARD\n");
        return (0);
    }
    else if (checkVisa(digitCount, leadingDigits))
    {
        printf("VISA\n");
        return (0);
    }
    else
    {
        printf("INVALID\n");
        return (0);
    }
}

int checkDigitLength(long input)
{
    int i = 0;
    while (input >= 1) 
    {
        input /= 10;
        i++;
    }

    return i;
}

bool passesLuhnAlgorithm(long cardNumber, int length)
{
    int digits[length];
    int digitCount = 0;

    int singleTotal = 0;
    int doubleDigitCount = length % 2 == 0 ? length / 2 : (length - 1) / 2;
    int doubledArray[doubleDigitCount];
    
    while (digitCount < length)
    {
        int digit = cardNumber % 10;
        // returns in reverse order
        digits[digitCount] = digit;
        cardNumber /= 10;
        digitCount++;
    }

    // track doubledArray counter seperately to avoid range overflow
    int doubledArrayCounter = 0;
    for (int index = 0; index < length; index++)
    {
        if (index % 2 == 0)
        {
            singleTotal += (digits[index]);
        }
        else
        {
            doubledArray[doubledArrayCounter] = (digits[index] * 2);
            doubledArrayCounter++;
        }
    }
    int doubledTotal = calculateDoubledArrayTotal(doubledArray, doubleDigitCount);
    
    return (singleTotal + doubledTotal) % 10 == 0;
}

int calculateDoubledArrayTotal(int doubledArray[], int doubleDigitCount)
{
    int total = 0;
    for (int i = 0; i < doubleDigitCount; i++)
    {
        int num = doubledArray[i];
        // if over 9, first digit guarenteed to be 1
        num > 9 ? (total += (1 + (num % 10))) : (total += num);
    }

    return total;
}

int getFirstDigits(long cardNumber)
{
    long digits = cardNumber;
    while (digits > 99)
    {
        digits /= 10;
    }

    return digits;
}

bool checkAmericanExpress(int length, int firstDigits)
{
    if (length != 15)
    {
        return false;
    }

    if (firstDigits != 34 && firstDigits != 37)
    {
        return false;
    }

    return true;
}

bool checkMasterCard(int length, int firstDigits)
{
    if (length != 16)
    {
        return false;
    }

    if (firstDigits < 51 || firstDigits > 55)
    {
        return false;
    }
    
    return true;
}

bool checkVisa(int length, int firstDigits)
{
    if (length != 13 && length != 16)
    {
        return false;
    }

    int singleDigit = firstDigits / 10;
    if (singleDigit != 4)
    {
        return false;
    }
    
    return true;
}
