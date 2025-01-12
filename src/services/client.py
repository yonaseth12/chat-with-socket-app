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