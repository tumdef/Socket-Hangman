#!/usr/bin/env python3

import socket
import sys

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
        self.sock.sendall(bytes(message, 'ascii'))
        
    def get_message(self):
        received = str(self.sock.recv(1024), 'ascii')
        print(received)

if __name__ == "__main__":
    test = client()
    try:
        ex = input("enter some text: ")
        test.send_message(ex)
        test.get_message()
    except (OverflowError, IOError):
        print("somthings wrong...")
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        test.sock.close()