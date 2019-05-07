#!/usr/bin/env python3

import socket
import sys
import core_game_client
import json

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
        while 1:
            game = core_game_client.Game() # hangman list from core_game_cli
            print("\n   {}\n".format(usr.get_message())) # get dashes
            guess_left = usr.get_message()
            print("Guess(es) left: {}".format(guess_left))
            data = usr.sock.recv(1024)
            letter_storage = json.loads(data)
            print("Used letters: {}".format(repr(letter_storage)))
            guess = input("Guess: ").lower()
            usr.send_message(guess) # get guess and send to server
            if guess == "reset":
                continue
            guessinserver = int(usr.get_message())
            # print(guessinserver)
            game.check_letter(guessinserver, guess) # send boolean if guess is in server to client
            #check for answer type
            ans_type = usr.get_message()
            if ans_type == "we":
                print("Congrats! You win. You just guessed the whole word and get extra score!")
            elif ans_type == "w":
                print("Congrats! You win. You just guessed the whole word! but did not get extra score :(")

            #end game
            if usr.get_message() == "rox":
                while 1:
                    again = input("Play again? [y/n]: ").lower()
                    if not (again == "y" or again == "yes" or again == "n" or again == "no"):
                        print("command '{}' not regcognize".format(again))
                        continue
                    break
                if again == "y" or again == "yes":
                    usr.send_message("reset")
                    continue
                break
                

    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        usr.sock.close()