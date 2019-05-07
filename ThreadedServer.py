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
        game = core_game_server.Game(name) # new game
        print("{} | Player name: {}".format(cur_thread.name ,game.player_name))
        #initial
        self.request.sendall(bytes(game.dashes, 'utf-8'))
        time.sleep(0.1)
        # TODO: best score from db
        self.request.sendall(bytes(str(game.guesses_left), 'utf-8'))
        time.sleep(0.1)
        letter_storage = json.dumps(game.letter_storage)
        self.request.sendall(letter_storage.encode())
        time.sleep(0.1)
        #game loop
        while 1:
            guess = str(self.request.recv(1024), 'utf-8') # get guess from conn
            if not guess: break
            print("{} | Guess: {}".format(cur_thread.name ,guess))
            if guess == "reset":
                game.reset()
                continue
        # loop end

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