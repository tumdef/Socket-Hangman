import threading
import socketserver
import sys
import core_game_server
import json
import time

class SingleTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # init
        print("connection from: {} {}".format(self.client_address[0], self.client_address[1]))
        cur_thread = threading.current_thread()
        print(cur_thread)
        thread_count = threading.active_count()
        print("thread count: {}".format(thread_count))
        name = str(self.request.recv(1024), 'utf-8') # get name from conn
        game = core_game_server.Game(name) # new gmae
        #game loop
        #while game.guesses_left > 0 and not game.dashes == game._secret_word:
        self.request.sendall(bytes(game.dashes, 'utf-8'))
        time.sleep(0.1)
        #best score
        self.request.sendall(bytes(str(game.guesses_left), 'utf-8'))
        time.sleep(0.1)
        letter_storage = json.dumps(game.letter_storage)
        self.request.sendall(letter_storage.encode())
        time.sleep(0.1)
        guess = str(self.request.recv(1024), 'utf-8') # get guess from conn

        # game

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    ADDR = ("localhost", 9999)
    server = ThreadedTCPServer((ADDR), SingleTCPHandler)
    main_thread = threading.current_thread()
    try:
        print("server loop running on: {}".format(main_thread.name))
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        server.shutdown()