#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"
unsigned int getCharValue(char c);

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 790920;

// Hash table
node *table[N];

// dictionary count
int dictCount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int wordHash = hash(word);

    // early exit if nothing in bucket
    if (table[wordHash] == NULL)
    {
        return false;
    }

    node *n = table[wordHash];

    // loops through list until reach null
    while (true)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }

        if (n->next == NULL)
        {
            return false;
        }

        n = n->next;
    }


    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int len = strlen(word);
    unsigned int total = 0;

    // get the bucket based on first 3 letters
    if (len > 2)
    {
        total += (getCharValue(word[2]) - 1) * 676;
    }

    if (len > 1)
    {
        total += (getCharValue(word[1]) - 1) * 26;
    }

    total += getCharValue(word[0]);

    // have a bucket for each length of word starting with same 3 letters
    return total * len;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("File can not be opened.");
        return false;
    }

    char currentWord[LENGTH];

    while (fscanf(file, "%s", currentWord) == 1)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }

        int wordHash = hash(currentWord);
        strcpy(n->word, currentWord);

        // find words bucket and add to start of list
        if (table[wordHash] == NULL)
        {
            table[wordHash] = n;
            n -> next = NULL;
        }
        else
        {
            n -> next = table[wordHash];
            table[wordHash] = n;
        }

        dictCount++;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary
unsigned int size(void)
{
    return dictCount;
}

// Unloads dictionary from memory
bool unload(void)
{
    for (int i = 0; i <= N; i++)
    {
        // empty bucket early exit
        if (table[i] == NULL)
        {
            continue;
        }

        node *point = table[i];

        // move along list in bucket
        while (point != NULL)
        {
            node *temp = point;
            point = point->next;
            free(temp);
        }
        free(point);
    }

    return true;
}

// get char values
unsigned int getCharValue(char c)
{
    if (c == 39)
    {
        // return Apostrophe as z, least common letter
        return 26;
    }
    // case insensitive
    return c > 90 ? c - 96 : c - 64;
}
