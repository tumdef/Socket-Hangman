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
            wrong_count = usr.get_message()
            game.wrong_count = int(wrong_count)
            print("{}\n".format(game._hangman[game.wrong_count]))
            print("\n   {}\n".format(usr.get_message())) # get dashes
            guess_left = usr.get_message()
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
            game.chk_ans_type(ans_type)

            if game.chk_ans_type(ans_type): break
            is_in_secret = usr.get_message()
            game.check_guess(int(is_in_secret), guess)
            #end game
        # get scoreboard
        print("{}".format(usr.get_message()))

    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        usr.sock.close()