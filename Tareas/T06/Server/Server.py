import socket
from threading import Thread
import os
import pickle
import sys
from Room import Room
import json
from double_speed import double_speed

# initialize host and port
HOST = 'localhost'
PORT = 4000


class Server:

    def __init__(self, host=HOST, port=PORT):
        # initialize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)

        # set to non blocking
        self.sock.setblocking(False)

        # initialize list of rooms
        self.rooms = list()
        self.load_rooms()

        # clients in lobby
        self.clients_in_lobby = list()

        # accept connections
        accept = Thread(target=self.accept_connections)
        accept.daemon = True
        accept.start()

        # process conections (for some reason it does not work)
        # process = Thread(target=self.procesarCon)
        # process.daemon = True
        # process.start()

        print('Server started')

        while True:
            msg = input('->')
            if msg == 'quit':
                self.sock.close()
                sys.exit()

    def load_rooms(self):
        genres = os.listdir('./Canciones')
        for i in genres:
            r = Room(genre=i)
            self.rooms.append(r)

    def accept_connections(self):
        '''Thread to accept connections anytime '''
        print("Accept Connections started")
        while True:
            try:
                conn, addr = self.sock.accept()
                # conn.setblocking(False)
                print('{} has connected to the server'.format(addr))
                # receive user information
                user_data = self.recv_decode(conn)
                print('data received: {}'.format(user_data))

                username = user_data['username']

                response = {'Found': False, 'data': None}
                if username + '.json' in os.listdir('./users_db'):
                    user_data = self.get_user_data(username)
                    response['Found'] = True
                    response['data'] = user_data
                else:
                    # create database user
                    self.save_user_data(user_data)
                    response['Found'] = False

                # send back his info
                self.send_encode(conn, response)

                # send back everyone's info
                everyone_info = []
                for i in os.listdir('./users_db'):
                    this_name = i.replace('.json', '')
                    this_info = self.get_user_data(this_name)
                    everyone_info.append(this_info)

                self.send_encode(conn, everyone_info)

                # send rooms info
                rooms_info = [{'genre': r.genre,
                               'people': len(r.clients_here),
                               'songs': r.get_songs_names()} for r in self.rooms]
                self.send_encode(conn, rooms_info)

                # add to clients so it can receive chat messages
                self.clients_in_lobby.append(conn)

            except socket.error:
                pass

    def retr_file(self, conn, filename):
        '''Sends a file (given by its filename) to
        a socket'''
        print('Retr_file started')
        if os.path.isfile(filename):
            msg = 'EXISTS {}'.format(os.path.getsize(filename))
            conn.send(pickle.dumps(msg))
            user_response = pickle.loads(conn.recv(1024))
            if user_response[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    conn.send(bytes_to_send)
                    while bytes_to_send != "":
                        bytes_to_send = f.read(1024)
                        conn.send(bytes_to_send)
        else:
            conn.send('ERR ')

    def procesarCon(self):
        print("ProcesarCon started")
        while True:
            if len(self.clients_in_lobby) > 0:
                for c in self.clients_in_lobby:
                    try:
                        data = c.recv(1024)
                        if data:
                            print(pickle.loads(data))
                    except Exception as err:
                        print(err)

    def send_encode(self, conn, msg):
        '''Sends a message encoded '''
        try:
            conn.send(pickle.dumps(msg))
        except socket.error:
            print('Client invalid')

    def recv_decode(self, conn):
        '''Receives, decodes and returns data given a connection '''
        try:
            data = conn.recv(1024)
            if data:
                return pickle.loads(data)
        except socket.error:
            print('could not receive')

    def save_user_data(self, user_data):
        username = user_data['username']
        with open('./users_db/{}.json'.format(username), 'w') as file:
            json.dump(user_data, file)
        print('User data saved succesfully')

    def get_user_data(self, username):
        with open('./users_db/{}.json'.format(username), 'r') as file:
            user_data = json.load(file)

        return user_data

if __name__ == '__main__':
    server = Server()
