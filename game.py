#!/usr/bin/env python3

import random
import re

WORD_FILE = 'words.txt'

class Game(object):
    _hangman = [
        """
            -----
            |   |
                |
                |
                |
                |
            ---------
""",
        """
            -----
            |   |
            O   |
                |
                |
                |
            ---------
""",

        """
            -----
            |   |
            O   |
            |   |
                |
                |
            ---------
""",
        """
            -----
            |   |
            O   |
            |\  |
                |
                |
            ---------
""",
        """
            -----
            |   |
            O   |
           /|\  |
                |
                |
            ---------
""",
        """
            -----
            |   |
            O   |
           /|\  |
             \  |
                |
            ---------
""",
        """
            -----
            |   |
            O   |
           /|\  |
           / \  |
                |
            ---------
"""]

resetOption = """
Play again ?[y/n]
"""


def get_guess(self):
    dashes = "-" * len(secret_word)
    guesses_left = 6
    wrong_count = 0
    print(self._hangman[wrong_count] + "\n")
    while guesses_left > 0 and not dashes == secret_word:

        # Print the amount of dashes and guesses left
        print(dashes)
        print("Guess(es) left: " + str(guesses_left))

        # Ask for input
        guess = input("Guess:")

        # Check for number input
        num_contain = re.search("\d+", guess)
        
        # Check if user guess the whole word    
        if guess == secret_word:
            print("Congrats! You win. You just guessed the whole word!")
            print(self._hangman[wrong_count] + "\n")
            break

        # Invalid inputs
        elif len(guess) != 1:
            print("Your guess must have exactly one character!")
            print(self._hangman[wrong_count] + "\n")
        
        # input only alphabet     
        elif not guess.isalpha():
            print("Your guess can only contains alphabet!")
            print(self._hangman[wrong_count] + "\n")

        # the guess is in the secret word
        elif guess in secret_word:
            print("That letter is in the secret word!")
            print(self._hangman[wrong_count] + "\n")
            dashes = update_dashes(secret_word, dashes, guess)

        else:
            wrong_count += 1
            guesses_left -= 1
            print("That letter is not in the secret word!\n")
            print(self._hangman[wrong_count] + "\n")

    # User loses
    if guesses_left < 1:
        print("You lose. The word was: " + str(secret_word))

    # User wins
    else:
        print("Congrats! You win. The word was: " + str(secret_word))

# updates the string of dashes
def update_dashes(secret, cur_dash, rec_guess):
    result = ""

    for i in range(len(secret)):
        if secret[i] == rec_guess:
            result = result + rec_guess # # Adds guess to string if guess is correctly

        else:
            # Add the dash at index i to result if it doesn't match the guess
            result = result + cur_dash[i]
    
    return result

if __name__ == "__main__" :
    # word list
    # words = ["bob", "baab", "burp", "apple"]
    wordlist = open(WORD_FILE, 'r').readlines()
    words = [word.strip() for word in wordlist]

    # random for a word in the list above
    secret_word = random.choice(words)
    # game
    get_guess(Game)

    while True :
        tmp = input(resetOption)
        if tmp == "n":
            print("BYE")
            break
        elif tmp == "y":
            secret_word = random.choice(words)
            print("Let's play again!")
            get_guess(Game)
        else :
            print("Input only y or n \n")

