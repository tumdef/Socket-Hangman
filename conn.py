#!/usr/bin/env python3

import socket
import sys
import core_game_client

class client():

    def __init__(self):
        # Create a socket and establish a connection
        print("connecting...")
        ADDR = ("localhost", 9999)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)
        print("connect to {}".format(ADDR))
        print("connection established...")

    def send_message(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))
        
    def get_message(self):
        received = str(self.sock.recv(1024), 'utf-8')
        return received

if __name__ == "__main__":
    usr = client()
    try:
        name = input("Please enter your name: ")
        usr.send_message(name)
        game = core_game_client.Game() # hangman list from core_game_cli
        while 1:
            while 1:
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
                if guess == "reset":
                    continue
                #check_letter
                guessinserver = int(usr.get_message())
                game.check_letter(guessinserver, guess) # send boolean if guess is in server to client
                #check for answer type
                ans_type = usr.get_message()
                if game.chk_ans_type(ans_type): break
                #check if in secret word
                is_in_secret = usr.get_message()
                game.check_guess(int(is_in_secret), guess)

                #check if game is end
                is_end = usr.get_message()
                if is_end == "running":
                    continue
                elif is_end == "lose":
                    secret_word = usr.get_message()
                    print("You lose. The word was: {}".format(secret_word))
                    break
                elif is_end == "win":
                    secret_word = usr.get_message()
                    print("Congrats! You win. The word was: {}".format(secret_word))
                    break
            #end game
            # get scoreboard
            print("{}".format(usr.get_message()))
            if usr.get_message() == "rox":
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
                break
    

    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        usr.sock.close()