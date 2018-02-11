import socket
from sys import exit
from threading import Thread
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QWidget
from PyQt5.QtGui import QColor
import pickle

# initialize host and port
HOST = 'localhost'
PORT = 4000


class Client(QWidget):

    def __init__(self, host=HOST, port=PORT):
        super().__init__()
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = False

    def connect_to_server(self):
        self.connection = True
        try:
            # connect to the server
            self.sock.connect(((self.host, self.port)))

        except socket.error:
            print('It was not possible to make the connection')
            self.connection = False
            exit()

    def connect_to_chat(self):
        receiver = Thread(target=self.hear_messages)
        receiver.setDaemon(True)
        receiver.start()

    def hear_messages(self):
        while self.connection:
            data = self.sock.recv(1024)

    def send_message(self, message):
        final_message = '{}: {}'.format(self.username, message)

    def send_encode(self, msg):
        '''Sends a message encoded '''
        try:
            self.sock.send(pickle.dumps(msg))
            print('sent: {}'.format(msg))
        except:
            pass

    def recv_decode(self):
        try:
            data = self.sock.recv(1024)
            if data:
                return pickle.loads(data)
        except socket.error:
            print('It was not possible to receive data from server')
