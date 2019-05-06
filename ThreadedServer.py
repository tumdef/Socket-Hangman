import threading
import socketserver
import sys

class SingleTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # run game here
        print("connection from: {} {}".format(self.client_address[0], self.client_address[1]))
        cur_thread = threading.current_thread()
        print(cur_thread)
        thread_count = threading.active_count()
        print("thread count: {}".format(thread_count))
        data = str(self.request.recv(1024), 'ascii')
        response = bytes("{}: {}".format(cur_thread.name, data.upper()), 'ascii')
        self.request.sendall(response)
        

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