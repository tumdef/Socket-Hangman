import random
from collections import Counter

class Game(object):
    _best_score = 0
    _hangman = [
        """
            -----
            |   |
                |
                |
                |
                |
            ---------""",
        """
            -----
            |   |
            O   |
                |
                |
                |
            ---------""",

        """
            -----
            |   |
            O   |
            |   |
                |
                |
            ---------""",
        """
            -----
            |   |
            O   |
            |\  |
                |
                |
            ---------""",
        """
            -----
            |   |
            O   |
           /|\  |
                |
                |
            ---------""",
        """
            -----
            |   |
            O   |
           /|\  |
             \  |
                |
            ---------""",
        """
            -----
            |   |
            O   |
           /|\  |
           / \  |
                |
            ---------"""]

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
        secret_word = random.choice(words)
        dashes = "-" * len(secret_word)
        guesses_left = 6
        wrong_count = 0
        correct_cnt = 0
        letter_storage = []
        print(self._hangman[wrong_count] + "\n")
        while guesses_left > 0 and not dashes == secret_word:

            # Print the amount of dashes and guesses left
            print(dashes)
            print("Best score: " + str(self._best_score))
            print("Guess(es) left: " + str(guesses_left))
            print("Used letters: " + " ".join(str(x) for x in letter_storage) + "\n")
            # Ask for input
            guess = input("Guess (To reset type resetgame): ").lower()

            # Check if user guess the whole word    
            if guess == secret_word:
                print("Congrats! You win. You just guessed the whole word!")
                print(self._hangman[wrong_count] + "\n")
                if correct_cnt < (len(secret_word))/2:
                    correct_cnt = len(secret_word)
                else :
                    correct_cnt = len(Counter(secret_word).keys())
                break

            #resetGame
            elif guess == "resetgame":
                break
        
            # input only alphabet     
            elif not guess.isalpha():
                print("Your guess can only contains alphabet!")
                print(self._hangman[wrong_count] + "\n")

            for d in range(len(guess)):

                #checking if letter has been already used
                if guess[d] in letter_storage:
                    print("You have already guessed that letter! ( "+guess[d]+" )")

                # the guess is in the secret word
                elif guess[d] in secret_word:
                    correct_cnt += 1
                    print("That letter ( "+guess[d]+" ) is in the secret word!")
                    print(self._hangman[wrong_count] + "\n")

                    dashes = Game.update_dashes(self,secret_word, dashes, guess[d])

                else:
                    wrong_count += 1
                    guesses_left -= 1
                    print("That letter ( "+guess[d]+" ) is not in the secret word!\n")
                    print(self._hangman[wrong_count] + "\n")
                
                # add guessed letter to a list
                if guess[d] not in letter_storage:
                    letter_storage.append(guess[d])

        #RESETGAME
        if guess == "resetgame":
            print("####### RESET GAME #######")

        # User loses
        elif guesses_left < 1:
            print("You lose. The word was: " + str(secret_word))

        # User wins
        else:
            print("Congrats! You win. The word was: " + str(secret_word))
            print("Score : "+ str(correct_cnt + guesses_left))
            if self._best_score < (correct_cnt + guesses_left):
                self._best_score = (correct_cnt + guesses_left)
                print("Congrats! You got the new best. The best score is: " + str(self._best_score))

WORD_FILE = 'words.txt'
if __name__ == "__main__" :
    # word list
    # words = ["bob", "baab", "burp", "apple"]
    wordlist = open(WORD_FILE, 'r').readlines()
    words = [word.strip() for word in wordlist]
    Game.newGame(Game)
    while True:
        tmp = input("Play again ?[y/n]: ").lower()
        if tmp == "n":
            print("Your best left is: " + str(Game._best_score))
            print("BYE")
            break
        elif tmp == "y":
            print("\n\n\n"+"Let's play again!\n")
            Game.newGame(Game)
        else :
            print("Input only y,Y or n,N \n")
