import random

class Game(object):
    _best_left = 0
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
        letter_storage = []
        print(self._hangman[wrong_count] + "\n")
        while guesses_left > 0 and not dashes == secret_word:

            # Print the amount of dashes and guesses left
            print(dashes)
            print("Best left: " + str(self._best_left))
            print("Guess(es) left: " + str(guesses_left))

            # Ask for input
            guess = input("Guess (To reset type resetgame): ").lower()
        
            # Check if user guess the whole word    
            if guess == secret_word:
                print("Congrats! You win. You just guessed the whole word!")
                print(self._hangman[wrong_count] + "\n")
                break
         
            #resetGame
            elif guess == "resetgame":
                break

            # Invalid inputs
            elif len(guess) != 1:
                print("Your guess must have exactly one character!")
                print(self._hangman[wrong_count] + "\n")
        
            # input only alphabet     
            elif not guess.isalpha():
                print("Your guess can only contains alphabet!")
                print(self._hangman[wrong_count] + "\n")

            #checking if letter has been already used
            elif guess in letter_storage:
                print("You have already guessed that letter!")

            # the guess is in the secret word
            elif guess in secret_word:
                print("That letter is in the secret word!")
                print(self._hangman[wrong_count] + "\n")
                dashes = Game.update_dashes(self,secret_word, dashes, guess)

            else:
                wrong_count += 1
                guesses_left -= 1
                print("That letter is not in the secret word!\n")
                print(self._hangman[wrong_count] + "\n")

            # add guessed letter to a list
            letter_storage.append(guess)

        #RESETGAME
        if guess == "resetgame":
            print("####### RESET GAME #######")

        # User loses
        elif guesses_left < 1:
            print("You lose. The word was: " + str(secret_word))

        # User wins
        else:
            print("Congrats! You win. The word was: " + str(secret_word))
            if self._best_left < guesses_left:
                self._best_left = guesses_left
                print("Congrats! You got the new best. The best left is: " + str(self._best_left))

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
            print("Your best left is: " + str(Game._best_left))
            print("BYE")
            break
        elif tmp == "y":
            print("\n\n\n"+"Let's play again!\n")
            Game.newGame(Game)
        else :
            print("Input only y,Y or n,N \n")
