import socket
import threading
import time

class Server():
    def __init__(self, PORT = None):
        self.PORT = PORT if PORT else 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.set_address(self.SERVER, self.PORT)

        self.HEADER_LENGTH = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.connected_clients = {}
        
        self.message_to_send = "Message to All Clients"
        self.sendbtn_pressed = False

        self.server = self.create_server(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)


    def set_address(self, SERVER, PORT):
        self.ADDR = (SERVER, PORT)

    def create_server(self, address_family, socket_kind):
        return socket.socket(address_family, socket_kind)
    
    def refer_server_callbacks(self, callback_functions):
        self.server_callback_functions = callback_functions
    
    def start(self):
        print("[STARTING] Server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        self.initiate_request_handler()

    def initiate_request_handler(self):
        admin_thread = threading.Thread(target=self.server_admin)
        admin_thread.start()
        while True:
            conn, address = self.server.accept()
            new_thread = threading.Thread(target=self.handle_client, args=(conn, address))
            new_thread.start()
            
    def server_admin(self):
        try:
            is_alive = True
            while is_alive:
                if self.sendbtn_pressed:
                    if self.message_to_send:
                        if self.message_to_send == self.DISCONNECT_MESSAGE:
                            is_alive = False
                            self.server_callback_functions.user_has_disconnected()
                            self.server.close()
                        self.send(self.message_to_send)
                    self.sendbtn_pressed = False
                time.sleep(1)
            
        except Exception as e:
            print("Connection has been lost")
            
    def send(self, message):
        message = message.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.broadcast_message(None, send_length, message)
            
            
    def handle_client(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        self.connected_clients[threading.current_thread().ident] = (conn, address)
        is_alive = True
        try:
            while is_alive:
                message_leng_encoded = conn.recv(self.HEADER_LENGTH)
                message_leng = message_leng_encoded.decode(self.FORMAT)
                if message_leng:                                        # There is an automatic blank message sent during connection initiation
                    message_length = int(message_leng)
                    message_encoded = conn.recv(message_length)
                    message = message_encoded.decode(self.FORMAT)
                    if message == self.DISCONNECT_MESSAGE:
                        is_alive = False
                        self.server_callback_functions.user_has_disconnected()
                        conn.close()
                    else:
                        self.server_callback_functions.receive_message(address, message)
                    print(f'[NEW MESSAGE] from {address} : {message}')
                    # Broadcast the message to all other clients
                    try:
                        self.server_callback_functions.receive_message(message)
                        self.broadcast_message(conn, message_leng_encoded, message_encoded)
                    except e:
                        print(f'[BROADCAST ERROR] {e}')
            conn.close()
            print(f'[CLOSE CONNECTION] {address} is disconnected.')
            del self.connected_clients[threading.current_thread().ident]
        except Exception as e:
            self.server_callback_functions.user_has_disconnected()
            conn.close()
        
    
    def broadcast_message(self, source_conn, message_length_enc, message_enc):
        for thread in threading.enumerate():        # Iterating over all current threads
            if thread.ident in self.connected_clients:
                if self.connected_clients[thread.ident][0] != source_conn:
                    self.connected_clients[thread.ident][0].send(message_length_enc)
                    self.connected_clients[thread.ident][0].send(message_enc)
            

    def count_active_users(self):
        return threading.activeCount() - 2          # One is main thread and the other is for server_send_handler