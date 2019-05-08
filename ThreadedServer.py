import threading
import socketserver
import sys
import core_game_server
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
                self.request.sendall(bytes("running", 'utf-8')) #send back game status
                time.sleep(0.1)
                #game loop

                self.request.sendall(bytes(str(game.wrong_count), 'utf-8')) # send wrong_count
                time.sleep(0.1)

                self.request.sendall(bytes(game.dashes, 'utf-8')) # send dashed
                time.sleep(0.1)
                
                self.request.sendall(bytes(str(game.guesses_left), 'utf-8')) # send guess_left
                time.sleep(0.1)

                guess = str(self.request.recv(1024), 'utf-8') # get guess from conn
                if not guess: break
                print("{} | Guess: {}".format(cur_thread.name ,guess))
                if guess == "reset": break

                is_whole = game.is_whole(guess)
                print("{} | ans type: {}".format(cur_thread.name, is_whole))

                self.request.sendall(bytes(str(is_whole), 'utf-8')) # send type of guess
                time.sleep(0.1)

                if is_whole == 'we' or is_whole == 'w': break

                elif is_whole == 'single':

                    if game.check_letter(guess):
                        self.request.sendall(bytes('1', 'utf-8')) # never guess this letter
                        time.sleep(0.1)

                        is_in_secret = game.check_guess(guess)
                        print(is_in_secret)
                        self.request.sendall(bytes(str(is_in_secret), 'utf-8')) # send guess right or wrong
                        time.sleep(0.1)
                    else:   
                        self.request.sendall(bytes('0', 'utf-8'))
                        time.sleep(0.1)

            #end
            if guess == "reset":
                game.reset()
                continue
            # User loses
            if game.guesses_left < 1:
                self.request.sendall(bytes("lose", 'utf-8')) #send back game status
                time.sleep(0.1)
            # User wins
            else:
                self.request.sendall(bytes("win", 'utf-8')) #send back game status
                time.sleep(0.1)

            self.request.sendall(bytes(game._secret_word, 'utf-8')) #send back secret word
            time.sleep(0.1)

            # Game end | call DBs functions to show scoreboard
            scoretxt = "Your score is {} points.".format(str(game.player_score))
            self.request.sendall(bytes(scoretxt, 'utf-8'))
            time.sleep(0.1)
            game.update_score(game.player_name, game.player_score)
            board = game.show_scoreboard()
            self.request.sendall(bytes(board, 'utf-8'))
            print("{} | Printed scoreboard in client".format(cur_thread.name))
            time.sleep(0.1)

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