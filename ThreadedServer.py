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
        while 1:
            print("{} | Secret word is: {}".format(cur_thread.name ,game._secret_word))
            
            while game.guesses_left > 0 and not game.dashes == game._secret_word:
                #game loop
                self.request.sendall(bytes(game.dashes, 'utf-8'))
                time.sleep(0.1)
                # TODO: best score from db
                self.request.sendall(bytes(str(game.guesses_left), 'utf-8'))
                time.sleep(0.1)
                letter_storage = json.dumps(game.letter_storage)
                self.request.sendall(letter_storage.encode())
                time.sleep(0.1)
                guess = str(self.request.recv(1024), 'utf-8') # get guess from conn
                if not guess: break
                print("{} | Guess: {}".format(cur_thread.name ,guess))
                if guess == "reset":
                    game.reset()
                    continue
                if game.check_letter(guess):
                    self.request.sendall(bytes('1', 'utf-8')) # never guess this letter
                    time.sleep(0.1)

                    is_whole = game.check_guess(guess)
                    print("{} | ans type: {}".format(cur_thread.name, is_whole))
                    self.request.sendall(bytes(is_whole, 'utf-8')) # send type of guess
                    time.sleep(0.1)
                    if is_whole: break
                else:
                    self.request.sendall(bytes('0', 'utf-8'))
                    time.sleep(0.1) #send back error message

            self.request.sendall(bytes("rox", 'utf-8')) # reset or exit
            end_ans = str(self.request.recv(1024), 'utf-8')
            if end_ans == "reset":
                game.reset()
                continue
            break
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