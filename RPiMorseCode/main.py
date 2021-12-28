from CharNotInMorseException import CharNotInMorseException
import RPi.GPIO as GPIO
from time import sleep
import pickle
import sys

## Read in file data to dictionary
# return dict
def readToDict():
    ## Open "morse.dat" in read binary mode
    while True:
        try:
            infile = open("morse.dat", "rb")
            break
        except FileNotFoundError:
            ## If the file isn't already created, create it
            print("[INFO] \"morse.dat\" created in working directory.")
            createMorseFile()

    ## @var dict empty dictionary to store morse code
    dict = {}

    while True:
        try:
            ## Load in data line, and store it in @var dict
            input = pickle.load(infile)
            key, value = input.split(" : ")
            dict[key] = value
        except EOFError:
            break

    ## Close input stream
    infile.close()

    ## Return dict containing morse code
    return dict

## Convert alphanumeric input into morse code
# @param word alphanumeric word input
# @param dict file containing morse code derivatives
def wordMorse(word, dict):
    for char in word:
        ## Check if character is in dictionary
        # If in dictionary proceed to obtain value
        # otherwise, throw an exception indicating its absence
        if char in dict:
            value = dict[char]

            for sym in value:
                ## Decrypt the character coding:
                # "-" : indicates 1 unit space
                # digit: indicates on time
                if sym == "-":
                    sleep(1)
                else:
                    sym = eval(sym)
                    GPIO.output(26, GPIO.HIGH)
                    sleep(sym)
                    GPIO.output(26, GPIO.LOW)
            ## Observe 3 space units at end of letter
            sleep(3)

        else:
            raise CharNotInMorseException(char)

    ## Observe 7 space units (3+4=7) at end of word
    sleep(4)

## Create morse file: morse.dat
def createMorseFile():
        morse_code = ["a : 1-3", "b : 3-1-1-1", "c : 3-1-3-1", "d : 3-1-1", \
        "e : 1", "f : 1-1-3-1", "g : 3-3-1", "h : 1-1-1-1", \
        "i : 1-1", "j : 1-3-3-3", "k : 3-1-3", "l : 1-3-1-1", \
        "m : 3-3", "n : 3-1", "o : 3-3-3", "p : 1-3-3-1", "q : 3-3-1-3", \
        "r : 1-3-1", "s : 1-1-1", "t : 3", "u : 1-1-3", "v : 1-1-1-3", \
        "w : 1-3-3", "x : 3-1-1-3", "y : 3-1-3-3", "z : 3-3-1-1", "1 : 1-3-3-3-3", \
        "2 : 1-1-3-3-3", "3 : 1-1-1-3-3", "4 : 1-1-1-1-3", "5 : 1-1-1-1-1", \
        "6 : 3-1-1-1-1", "7 : 3-3-1-1-1", "8 : 3-3-3-1-1", "9 : 3-3-3-3-1", \
        "0 : 3-3-3-3-3"]

        outfile = open("morse.dat", "wb")
        # write to binary file
        for line in morse_code:
            pickle.dump(line ,outfile)

        outfile.close()

def main():
    print("[INFO] GPIO 26 (pin 37) used as output pin.")
    ## Raspberry Pi config
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    ## Derive morse code from dict file
    morseCodeDict = readToDict()

    while True:
        word = input(">> Enter word to encrypt: ")

        ## Feel free to expand this definition to encrypt many
        # words in a sentence:
        # words = word.split()
        # for word in words:

        try:
            ## Output morse code representation of word input
            wordMorse(word.lower(), morseCodeDict)
        except CharNotInMorseException as ex:
            print("[ALERT] The following character is undefined: ", ex.getChar())

        control = input(">> Enter another word? (Y/N)").upper()

        if control == "N" or "NO":
            ## Deallocate RPi resources
            GPIO.cleanup()
            break

if __name__ == '__main__':
    main()
