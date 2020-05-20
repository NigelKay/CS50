from cs50 import get_int


def main():
    bricks = 0
    while bricks < 1 or bricks > 8:
        bricks = get_int("Height: ")

    buildPyramid(bricks)


def buildPyramid(bricks):
    for i in range(bricks + 1):
        buildLine(i, bricks)


def buildLine(brickCount, total):
    if brickCount > 0:
        midBuffer = 2
        spaceBuffer = total - brickCount

        printCharacter(spaceBuffer, ' ')
        printCharacter(brickCount, '#')
        printCharacter(midBuffer, ' ')
        printCharacter(brickCount, '#', True)


def printCharacter(num, character, lineEnd=False):
    print(character * num, end="")
    if lineEnd:
        print()


main()
