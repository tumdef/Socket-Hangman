#!/usr/bin/env python3

import socket
import sys
import core_game_client
import time

class client():

    def __init__(self):
        # Create a socket and establish a connection
        print("connecting...")
        ADDR = ("localhost", 9999)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)
        print("connect to {}".format(ADDR))
        print("connection established...\n")
        client.welcome_message(self)

    def send_message(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))
        
    def get_message(self):
        received = str(self.sock.recv(1024), 'utf-8')
        return received

    def welcome_message(self):
        print("Welcome to Hangman game!")
        print("while playing type 'reset' anytime to reset the game")
        print("Enter your name to continue...")

if __name__ == "__main__":
    usr = client()
    try:
        while 1:
            name = input("Please enter your name: ")
            if name == "reset":
                print("")
                usr.welcome_message()
                continue
            break
        usr.send_message(name)
        game = core_game_client.Game() # hangman list from core_game_cli
        while 1:
            #check if game is end
            is_end = usr.get_message()
            if is_end == "running":

                wrong_count = usr.get_message()

                game.wrong_count = int(wrong_count)

                dashes = usr.get_message()

                guess_left = usr.get_message()

                print("{}\n".format(game._hangman[game.wrong_count]))
                print("\n   {}\n".format(dashes)) # get dashes
                print("Guess(es) left: {}".format(guess_left))
                print("Used letters: {}".format(" ".join(str(x) for x in game.letter_storage) + "\n"))

                guess = input("Guess: ").lower()
                usr.send_message(guess) # get guess and send to server
                # user want to reset
                if guess == "reset":
                    game.reset()
                    continue

                #check for answer type
                ans_type = usr.get_message()
                if not game.chk_ans_type(ans_type): #single type will do the if

                    #check_letter
                    guessinserver = int(usr.get_message())
                    if game.check_letter(guessinserver, guess): # send boolean if guess is in server to client
                        pass #invalid guess
                    else:
                        #check if in secret word
                        is_in_secret = usr.get_message()
                        game.check_guess(int(is_in_secret), guess)
                continue

            elif is_end == "lose":
                secret_word = usr.get_message()
                print("You lose. The word was: {}".format(secret_word))

            elif is_end == "win":
                secret_word = usr.get_message()
                if ans_type == "we":
                    print("Congrats! You win. You just guessed the whole word and get extra score!", end="")
                elif ans_type == "w":
                    print("Congrats! You win. You just guessed the whole word! but did not get extra score :(", end="")
                else:
                    print("Congrats! You win.", end="")
                print(" The word was: {}".format(secret_word))
            
            #end game
            # get score of current round
            print("{}".format(usr.get_message()))
            # get scoreboard
            print("{}".format(usr.get_message()))
            while 1:
                again = input("Play again? [y/n]: ").lower()
                if not (again == "y" or again == "yes" or again == "n" or again == "no"):
                    print("command '{}' not regcognize".format(again))
                    continue
                break
            if again == "y" or again == "yes":
                usr.send_message("reset")
                game.reset()
                continue
            usr.send_message("x")
            break


    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        usr.sock.close()