#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <cs50.h>

int getArgLength(char *key);
bool checkWholeAlphabet(char *alphabet, char *key);

int main(int argc,  char *argv[])
{
    if (argc != 2)
    {
        printf("You must supply exactly 1 argument.");
        return 1;
    }

    char *key = argv[1];
    int keyLength = getArgLength(key);
    char *alphabet = "abcdefghijklmnopqrstuvwxyz";

    if (keyLength != 26)
    {
        printf("Invalid Key. The key should be exactly 26 characters long.");
        return 1;
    }

    if (!checkWholeAlphabet(alphabet, key))
    {
        printf("Invalid key. The key does not contain every letter of the alphabet.");
        return 1;
    }

    int keyMap[26];
    // create an array of differences between alphabet and given key
    for (int i = 0; i < 26; i++)
    {
        // handle upper and lowercase
        keyMap[i] = key[i] > 96 ? key[i] - alphabet[i] : (key[i] + 32) - alphabet[i];
    }

    char *plain = get_string("plaintext: ");
    printf("ciphertext: ");

    int counter = 0;
    while (plain[counter] != '\0')
    {
        char c = plain[counter];
        //return non alpha
        if (c < 65 || (c > 90 && c < 97) || c > 122)
        {
            printf("%c", c);
        }
        else
        {
            int buffer = 0;
            // calculate keyMap position
            if (c > 96)
            {
                buffer = c - 97;
            }
            else if (c > 64 && c < 91)
            {
                buffer = c - 65;
            }

            char newLetter = c + keyMap[buffer];
            printf("%c", newLetter);
        }

        counter++;
    }
    printf("\n");
    return 0;
}

int getArgLength(char *key)
{
    int i;
    for(i=0; key[i]!='\0'; i++);
    return i;
}

bool checkWholeAlphabet(char *alphabet, char *key)
{
    for (int i = 0; i < 26; i++)
    {
        // check upper and lowercase
        if (!strchr(key, alphabet[i]) && !strchr(key, alphabet[i] - 32))
        {
            return false;
        }
    }
    return true;
}

