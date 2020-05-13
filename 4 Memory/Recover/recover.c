#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

bool checkFourthByte(unsigned char c);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("File can not be opened.");
        return 1;
    }

    int imageCounter = 0;
    int byteBlock = 512;

    // init new recovery files
    FILE *newImageFile = NULL;

    // read in blocks of 512 bytes
    unsigned char block[byteBlock];
    while (fread(block, byteBlock, 1, file))
    {
        if (
            block[0] == 0xff &&
            block[1] == 0xd8 &&
            block[2] == 0xff &&
            checkFourthByte(block[3])
        )
        {
            // close and make new file after discovering jpeg signature
            if (newImageFile != NULL)
            {
                fclose(newImageFile);
            }

            // increment file naming in ###.jpg format
            char filename[8];
            sprintf(filename, "%03d.jpg", imageCounter);

            newImageFile = fopen(filename, "w");
            imageCounter++;
        }

        if (newImageFile != NULL)
        {
            fwrite(block, byteBlock, 1, newImageFile);
        }
    }

    if (newImageFile != NULL)
    {
        fclose(newImageFile);
    }

    fclose(file);
    return 0;
}

bool checkFourthByte(unsigned char c)
{
    // valid 4th bytes for JPEG
    unsigned char valid[16] = {0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef};

    for (int i = 0; i < 16; i++)
    {
        if (c == valid[i])
        {
            return true;
        }
    }

    return false;
}