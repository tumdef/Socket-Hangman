#!/usr/bin/env python3

import random


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


def get_guess(self):
    dashes = "-" * len(secret_word)
    guesses_left = 6
    wrong_count = 0

    while guesses_left > -1 and not dashes == secret_word:

        # Print the amount of dashes and guesses left
        print(dashes)
        print(str(guesses_left))

        # Ask for input
        guess = input("Guess:")

        # Check if user guess the whole word
        if guess == secret_word:
            print("Congrats! You win. You just guessed the whole word!")
            break

        # Invalid inputs
        elif len(guess) != 1:
            print("Your guess must have exactly one character!")

        # the guess is in the secret word
        elif guess in secret_word:
            print("That letter is in the secret word!")
            dashes = update_dashes(secret_word, dashes, guess)

        else:
            print("That letter is not in the secret word!\n")
            print(self._hangman[wrong_count] + "\n")
            wrong_count += 1
            guesses_left -= 1

    # User loses
    if guesses_left < 0:
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

words = ["bob", "baab", "burp", "apple"]

secret_word = random.choice(words)
get_guess(Game)