#!/usr/bin/env python3

import random
from collections import Counter
import linecache

class Game:
    _userName = ""
    _best_score = 0
    _hangman = (
        """
             _____
             |  \|
                 |
                 |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
                 |
                 |
                 |
            =========""",

        """
             _____
             |  \|
             O   |
             |   |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
             |\  |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
              \  |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
            / \  |
                 |
            =========""")

    def update_dashes(self,secret, cur_dash, rec_guess):
        result = ""

        for i in range(len(secret)):
            if secret[i] == rec_guess:
                result = result + rec_guess #Adds guess to string if guess is correctly

            else:
                # Add the dash at index i to result if it doesn't match the guess
                result = result + cur_dash[i]
    
        return result

    def newGame(self):
        generate = random.randint(1, 734)
        secret_word = linecache.getline('words.txt', generate)[:-1]
        dashes = "-" * len(secret_word)
        guesses_left = 6
        wrong_count = 0
        correct_cnt = 0
        letter_storage = []
        print("{}\n".format(self._hangman[wrong_count]))

        """ 
        This loop will run until you win, lose or type "reset" 
        """#guess = input("Guess (To reset type resetgame): ").lower()
"""init"""  while guesses_left > 0 and not dashes == secret_word:
            # Print the amount of dashes and guesses left
            """print("\n   {}\n".format(dashes))
            print("Best score({}): {}".format(self._userName, str(self._best_score)))
            print("Guess(es) left: {}".format(guesses_left))
            print("Used letters: {}".format(" ".join(str(x) for x in letter_storage) + "\n"))
            """# Ask for input

          # Check if user guess the whole word
            if guess == secret_word:
                print("Congrats! You win. You just guessed the whole word!")
                if correct_cnt < (len(secret_word))/2:
                    correct_cnt = len(secret_word)
                    print("And get extra score!")
                else : #cheating
                    correct_cnt = len(Counter(secret_word).keys())
                break

            """#resetGame
            elif guess == "resetgame":
                print("####### RESET GAME #######")
                break"""
       
            else :

                for d in range(len(guess)):

                    #checking if guess_left is out
                    if guesses_left < 1 or correct_cnt >= len(Counter(secret_word).keys()):
                        break

                    #checking if letter has been already used
                    elif guess[d] in letter_storage:
                        print("You have already guessed the letter \"{}\"!".format(guess[d]))

                    # input only alphabet  
                    elif not guess[d].isalpha():
                        print("Your guess can only contains alphabet!")
                        print("\"{}\" is not an alphabet!".format(guess[d]))
                        letter_storage.append(guess[d])        
                    
                    else :
                        # the guess is in the secret word
                        if guess[d] in secret_word:
                            correct_cnt += 1
                            print("The letter {} is in the secret word!".format(guess[d]))

                            dashes = Game.update_dashes(self,secret_word, dashes, guess[d])

                        else:
                            wrong_count += 1
                            guesses_left -= 1
                            print("The letter {} is not in the secret word!".format(guess[d]))

                        # add guessed letter to letter_storage list    
                        letter_storage.append(guess[d])

            print("{}\n".format(self._hangman[wrong_count]))

            if guesses_left < 1 or correct_cnt >= len(Counter(secret_word).keys()):
                    break
        """
        end loop
        """

        """#user reset
        if guess == "resetgame":
            Game.newGame(self)"""

        # User loses
        elif guesses_left < 1:
            print("{}".format(dashes))
            print("Your guess is out")
            print("You lose. The word was: {}".format(secret_word))

        # User wins
        else:
            print("Congrats! You win. The word was: {}".format(secret_word))
            print("Your score : {}".format(correct_cnt + guesses_left))
            if self._best_score < (correct_cnt + guesses_left):
                self._best_score = (correct_cnt + guesses_left)
                print("Congrats! You got the new best. The best score is: {}".format(self._best_score))


        while True:
            #end game
            tmp = input("Play again ?[y/n]: ").lower()
            if tmp == "n":
                print("Your best left is: {}".format(self._best_score))
                print("BYE {}".format(self._userName))
                break
            elif tmp == "y":
                print("\n\n\nLet's play again!\n")
                Game(self._userName,self._best_score)
            else :
                print("command not regcognize\n")
            #sys.exit(0)