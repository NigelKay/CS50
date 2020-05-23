from cs50 import get_string


def main():
    string = get_string("Text: ")
    counts = getCounts(string)

    # Coleman-Liau Index
    # index = 0.0588 * L - 0.296 * S - 15.8
    l = (counts['letters'] / counts['words']) * 100
    s = (counts['sentences'] / counts['words']) * 100
    res = (0.0588 * l) - (0.296 * s) - 15.8
    roundedRes = round(res)

    printResult(roundedRes)


def getCounts(string):
    d = dict()
    letters = 0
    words = 1  # Counts last word
    sentences = 0

    for char in string:
        if char == ' ':
            words += 1
        elif char in ['.', '!', '?']:
            sentences += 1
        elif char.isalpha():
            letters += 1

    d['letters'] = letters
    d['words'] = words
    d['sentences'] = sentences

    return d


def printResult(roundedRes):
    if roundedRes < 1:
        print("Before Grade 1")
    elif roundedRes >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {roundedRes}")


main()
