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