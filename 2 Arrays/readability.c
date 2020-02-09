#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

struct TextValues
{
    int letters,
        words,
        sentences;
};
typedef struct TextValues TextStatistics;

TextStatistics getCounts(char *textInput);

int main(void)
{
    string textInput = get_string("Text: ");
    TextStatistics results;
    results = getCounts(textInput);

    // Coleman-Liau Index
    // index = 0.0588 * L - 0.296 * S - 15.8
    float l = ((float)results.letters / results.words) * 100;
    float s = ((float)results.sentences / results.words) * 100;
    float res = (0.0588 * l) - (0.296 * s) - 15.8;
    int roundedRes = round(res);

    if (roundedRes < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (roundedRes >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", roundedRes);
    }
}

TextStatistics getCounts(char *textInput)
{
    TextStatistics results;

    results.letters = 0;
    results.words = 1; // counts last word
    results.sentences = 0;

    int textLength = strlen(textInput);
    for (int i = 0; i < textLength; i++)
    {
        char c = textInput[i];

        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
        {
            results.letters++;
        }

        if (c == ' ')
        {
            results.words++;
        }

        if (c == '.' || c == '?' || c == '!')
        {
            results.sentences += 1;
        }
    }
    return results;
}
