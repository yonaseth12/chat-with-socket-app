import socket
import threading

class Server():
    def __init__(self, PORT):
        self.PORT = PORT if PORT else 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.set_address(self.SERVER, self.PORT)

        self.HEADER_LENGTH = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.connected_clients = {}

        self.server = self.create_server(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)


    def set_address(self, SERVER, PORT):
        self.ADDR = (SERVER, PORT)

    def create_server(self, address_family, socket_kind):
        return socket.socket(address_family, socket_kind)
    
    def start(self):
        print("[STARTING] Server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        self.initiate_request_handler()

    def initiate_request_handler(self):
        while True:
            conn, address = self.server.accept()
            new_thread = threading.Thread(target=self.handle_client, args=(conn, address))
            new_thread.start()

    def handle_client(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        self.connected_clients[threading.current_thread().ident] = (conn, address)
        is_alive = True
        while is_alive:
            message_leng_encoded = conn.recv(self.HEADER_LENGTH)
            message_leng = message_leng_encoded.decode(self.FORMAT)
            if message_leng:                                        # There is an automatic blank message sent during connection initiation
                message_length = int(message_leng)
                message_encoded = conn.recv(message_length)
                message = message_encoded.decode(self.FORMAT)
                if message == self.DISCONNECT_MESSAGE:
                    is_alive = False
                print(f'[NEW MESSAGE] from {address} : {message}')
                
                # Broadcast the message to all other clients
                self.broadcast_message(conn, message_leng_encoded, message_encoded)
        conn.close()
        print(f'[CLOSE CONNECTION] {address} is disconnected.')
        self.connected_clients.remove((conn, address))
    
    def broadcast_message(self, source_conn, message_length_enc, message_enc):
        for thread in threading.enumerate():        # Iterating over all current threads
            if thread.ident in self.connected_clients:
                if self.connected_clients[thread.ident][0] != source_conn:
                    self.connected_clients[thread.ident][0].send(message_length_enc)
                    self.connected_clients[thread.ident][0].send(message_enc)
            

    def count_active_users(self):
        return threading.activeCount() - 1