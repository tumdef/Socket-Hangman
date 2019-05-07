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
        game = core_game_client.Game() # hangman list from core_game_cli
        print("\n   {}\n".format(usr.get_message())) # get dashes
        guess_left = usr.get_message()
        print("Guess(es) left: {}".format(guess_left))
        data = usr.sock.recv(1024)
        letter_storage = json.loads(data)
        print("Used letters: {}".format(repr(letter_storage)))
        while 1:
            guess = input("Guess: ").lower()
            usr.send_message(guess) # get guess and send to server
            if guess == "reset":
                continue

    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        usr.sock.close()