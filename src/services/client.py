Client():
    def __init__(self, PORT):
        self.PORT = PORT if PORT else 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.set_address(self.SERVER, self.PORT)

        self.HEADER_LENGTH = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"


    def set_address(self, SERVER, PORT):
        self.ADDR = (SERVER, PORT)
        
    def initiate_request_handler(self):
        while True:
            conn, address = self.server.accept()
            new_thread = threading.Thread(target=self.handle_client, args=(conn, address))
            new_thread.start()
            
    def handle_client(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        is_alive = True
        while is_alive:
            message_leng = conn.recv(self.HEADER_LENGTH).decode(self.FORMAT)
            message_length = int(message_leng)
            message = conn.recv(message_length).decode(self.FORMAT)
            if message == self.DISCONNECT_MESSAGE:
                is_alive = False
            print(f'[NEW MESSAGE] from {address} : {message}')
        conn.close()

    def count_active_users(self):
        return threading.activeCount() - 1
        
    def initiate_request_handler(self):
        while True:
            conn, address = self.server.accept()
            new_thread = threading.Thread(target=self.handle_client, args=(conn, address))
            new_thread.start()