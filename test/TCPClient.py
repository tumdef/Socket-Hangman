#!/usr/bin/env python3

import socket
import sys
import re

HOST, PORT = "localhost", 9999
if len(sys.argv) < 2:
    slash = re.search("\./", sys.argv[0])
    if slash:
        print("Usage: {} <message>".format(sys.argv[0]))
        print("or python(3) {} <message>".format(sys.argv[0][2:]))
    else:
        print("Usage: ./{} <message>".format(sys.argv[0]))
        print("or python(3) {} <message>".format(sys.argv[0]))
    sys.exit()
else:
    data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))