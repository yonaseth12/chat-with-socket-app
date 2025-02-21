from binascii import Error
import socket
import threading
import time

class Client:

    def __init__(self, server_addr):
        self.SERVER = server_addr

        self.HEADER_LENGTH = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.sendbtn_pressed = False
        try:    
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.SERVER)
        except Exception as e:
            raise Error("Error has occurred while connecting to the server")
        
        self.start()

    def send(self, message):
        message = message.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


    def receive_handler(self):
        is_alive = True
        while is_alive:
            message_leng = self.client.recv(self.HEADER_LENGTH).decode(self.FORMAT)
            if message_leng:                                        # There is an automatic blank message sent during connection initiation
                message_length = int(message_leng)
                message = self.client.recv(message_length).decode(self.FORMAT)
                if message == self.DISCONNECT_MESSAGE:
                    is_alive = False
                print(f'[NEW MESSAGE] Incoming : {message}')


    def send_handler(self):
        try:
            while True:
                if self.sendbtn_pressed:
                    message_to_send = "Mesaage from client"
                    if message_to_send:
                        self.send(message_to_send)
                    self.sendbtn_pressed = False
                time.sleep(1)
                
        except Exception as e:
            print("Connection has been lost")

    def start(self):
        receiver_thread = threading.Thread(target=self.receive_handler)
        receiver_thread.start()
        sender_thread = threading.Thread(target=self.send_handler)
        sender_thread.start()