#include <stdio.h>
#include <math.h>

#include "helpers.h"

int calculateColour(int Gx, int Gy);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE *currentPixel = &image[i][j];
            float sum = currentPixel -> rgbtBlue + currentPixel -> rgbtGreen + currentPixel -> rgbtRed;
            int total = roundf(sum / 3);

            currentPixel -> rgbtBlue = total;
            currentPixel -> rgbtGreen = total;
            currentPixel -> rgbtRed = total;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newImage[i][j] = image[i][(width - 1) - j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];

    for (int baseY = 0; baseY < height; baseY++)
    {
        for (int baseX = 0; baseX < width; baseX++)
        {
            RGBTRIPLE pixelFamily[9];
            int counter = 0;

            // get the 3x3 grid surrounding the current x,y coordinate
            for (int gridY = (baseY - 1); gridY < baseY + 2; gridY++)
            {
                // discard all out of bounds indexes
                if (gridY >= 0 && gridY < height)
                {
                    for (int gridX = (baseX - 1); gridX < baseX + 2; gridX++)
                    {
                        if (gridX >= 0 && gridX < width)
                        {
                            pixelFamily[counter] = image[gridY][gridX];
                            counter++;
                        }
                    }
                }
            }

            RGBTRIPLE newPixel;

            float redCount = 0;
            float greenCount = 0;
            float blueCount = 0;

            for (int i = 0; i < counter; i++)
            {
                RGBTRIPLE pixel = pixelFamily[i];

                redCount += pixel.rgbtRed;
                greenCount += pixel.rgbtGreen;
                blueCount += pixel.rgbtBlue;
            }

            newPixel.rgbtRed = roundf(redCount / counter);
            newPixel.rgbtGreen = roundf(greenCount / counter);
            newPixel.rgbtBlue = roundf(blueCount / counter);

            // assign the pixel to a new array image to avoid diluting the image
            newImage[baseY][baseX] = newPixel;
        }
    }

    // copy in the new image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    RGBTRIPLE emptyPixel = {.rgbtBlue = 0, .rgbtGreen = 0, .rgbtRed = 0};

    // Sobel kernels
    int Gx[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int Gy[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};

    for (int baseY = 0; baseY < height; baseY++)
    {
        for (int baseX = 0; baseX < width; baseX++)
        {
            // default to 0's for edges
            RGBTRIPLE pixelFamily[9] = {emptyPixel};
            int counter = 0;

            // get the 3x3 grid surrounding the current x,y coordinate
            for (int gridY = (baseY - 1); gridY < baseY + 2; gridY++)
            {
                // discard all out of bounds indexes
                if (gridY >= 0 && gridY < height)
                {
                    for (int gridX = (baseX - 1); gridX < baseX + 2; gridX++)
                    {
                        if (gridX >= 0 && gridX < width)
                        {
                            pixelFamily[counter] = image[gridY][gridX];
                            counter++;
                        }
                        else
                        {
                            // leave as zero
                            counter++;
                        }
                    }
                }
                else
                {
                    // skip the row
                    counter += 3;
                }
            }

            int GxR = 0;
            int GyR = 0;
            int GxG = 0;
            int GyG = 0;
            int GxB = 0;
            int GyB = 0;


            for (int p = 0; p < counter; p++)
            {
                RGBTRIPLE cPixel = pixelFamily[p];
                int GxValue = Gx[p];
                int GyValue = Gy[p];

                GxR += cPixel.rgbtRed * GxValue;
                GyR += cPixel.rgbtRed * GyValue;

                GxG += cPixel.rgbtGreen * GxValue;
                GyG += cPixel.rgbtGreen * GyValue;

                GxB += cPixel.rgbtBlue * GxValue;
                GyB += cPixel.rgbtBlue * GyValue;
            }

            int newRed = calculateColour(GxR, GyR);
            int newGreen = calculateColour(GxG, GyG);
            int newBlue = calculateColour(GxB, GyB);

            RGBTRIPLE newPixel = {.rgbtBlue = newBlue, .rgbtGreen = newGreen, .rgbtRed = newRed};
            newImage[baseY][baseX] = newPixel;

        }

    }

    // copy in the new image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}

// apply the Sobel colour calculation
int calculateColour(int Gx, int Gy)
{
    double total = (Gx * Gx) + (Gy * Gy);
    double result = sqrt(total);

    if (result > 255)
    {
        result = 255;
    }

    return round(result);
}

