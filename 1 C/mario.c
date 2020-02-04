#include <cs50.h>
#include <stdio.h>

void buildPyramid(int bricks);
void buildLine(int brickCount, int total);
void printCharacter(int num, char character);

int main(void)
{
    int bricks = 0;
    while (bricks < 1 || bricks > 8) 
    {
        bricks = get_int("Height: ");
    }

    buildPyramid(bricks);
}

void buildPyramid(int bricks) 
{
    for (int i = 1; i <= bricks; i++)
    {
        buildLine(i, bricks);
    }
}

void buildLine(int brickCount, int total)
{
    if (brickCount > 0)
    {
        int midBuffer = 2;
        int buffer = total - brickCount;
        
        printCharacter(buffer, ' ');
        printCharacter(brickCount, '#');
        printCharacter(midBuffer, ' ');
        printCharacter(brickCount, '#');
        printf("\n");
    }
}

void printCharacter(int num, char character)
{
    for (int i = 0; i < num; i++)
    {
        printf("%c", character);
    }
}
