import socket
from sys import exit
from threading import Thread
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import (QApplication, QListWidgetItem, QWidget,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QStackedWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import pickle
import os
from Client import Client
from User import User


class Game(QStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # initialize client
        self.client = Client()

        # initialize user
        self.user = User()

        # other users received
        self.others = []

        # initiliaze room's info
        self.rooms_info = list()

        self.setUp_home()

        self.setCurrentIndex(0)

    def setUp_home(self):
        # Home page
        input_window = QWidget(self)
        login_btn = QPushButton('Log-in', input_window)
        login_btn.clicked.connect(self.on_loginButton_clicked)
        self.userNameText = QLineEdit(input_window)
        v_box = QVBoxLayout()
        v_box.addWidget(self.userNameText)
        v_box.addWidget(login_btn)
        input_window.setLayout(v_box)

        self.addWidget(input_window)

    def setUp_main_page(self):
        '''Creates a main page '''
        # main page
        main_page = QWidget(self)
        self.user_label = QLabel('User: {}'.format(self.user.get_username()), main_page)
        self.points_label = QLabel('Score: {}'.format(self.user.get_points()), main_page)
        clasification_label = QLabel('Clasification Table')

        main_page_v_box = QVBoxLayout()
        main_page_v_box.addWidget(self.user_label)
        main_page_v_box.addWidget(self.points_label)
        main_page_v_box.addWidget(clasification_label)

        # create clasification table
        for u in self.others:
            this_name = str(u['username'])
            this_points = str(u['points'])

            this_name_label = QLabel(this_name, main_page)
            this_points_label = QLabel(this_points, main_page)

            this_h_box = QHBoxLayout()
            this_h_box.addWidget(this_name_label)
            this_h_box.addWidget(this_points_label)

            main_page_v_box.addLayout(this_h_box)

        # create play and challenge btns
        play_btn = QPushButton('Play', main_page)
        challenge_btn = QPushButton('Challenge', main_page)

        play_btn.clicked.connect(self.on_playButton_clicked)

        # set graphiscs
        btns_h_box = QHBoxLayout()
        btns_h_box.addWidget(play_btn)
        btns_h_box.addWidget(challenge_btn)

        main_page_v_box.addLayout(btns_h_box)

        main_page.setLayout(main_page_v_box)

        self.addWidget(main_page)

    def setuUp_choose_page(self):
        # choose page
        choose_page = QWidget(self)
        choose_label = QLabel('CHOOSE A ROOM', choose_page)
        choose_layout = QVBoxLayout()
        choose_layout.addWidget(choose_label)

        for r in self.rooms_info:
            g = r['genre']
            n_people = str(r['people'])
            this_h_box = QHBoxLayout()
            this_btn = QPushButton(str(g), choose_page)
            this_btn.clicked.connect(self.on_genreButton_clicked)
            this_n_people = QLabel(n_people, choose_page)

            this_h_box.addWidget(this_btn)
            this_h_box.addWidget(this_n_people)
            choose_layout.addLayout(this_h_box)

        loading_label = QLabel('', choose_page)
        choose_layout.addWidget(loading_label)

        choose_page.setLayout(choose_layout)
        self.addWidget(choose_page)

    def on_genreButton_clicked(self):
        # check if I have the songs
        btn = self.sender()
        genre = btn.text()

        room_to_play = [d for d in self.rooms_info if d['genre'] == genre].pop()
        songs_to_play = room_to_play['songs']

    def receive_file(self, filename):
        '''Receives a file, and gives it the filename '''
        data = self.client.recv_decode()
        if data[:6] == 'EXISTS':
            filesize = int(data[6:])
            self.client.send_encode('OK')
            f = open('new_{}'.format(filename), 'wb')
            data = self.client.sock.recv(1024)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < filesize:
                data = self.client.sock.recv(1024)
                totalRecv += len(data)
                f.write(data)
            print('Download Complete')
            f.close()

    def on_playButton_clicked(self):
        self.setuUp_choose_page()
        self.setCurrentIndex(self.currentIndex() + 1)

    def on_loginButton_clicked(self):
        # get username and connect to server
        username = self.userNameText.text()
        self.user.set_username(username.lower())

        # connect to server
        self.client.connect_to_server()

        # send user data
        self.client.send_encode(self.user.__dict__)
        response = self.client.recv_decode()

        # if found, rewrite its info
        if response['Found']:
            print('User loaded from server')
            user_dict = response['data']
            self.user = User.from_dict(user_dict)

        # server should send everyone's info
        response_everyone_info = self.client.recv_decode()
        self.others.extend(response_everyone_info)

        # receive room's info
        response_rooms_info = self.client.recv_decode()
        self.rooms_info.extend(response_rooms_info)
        print('received: {}'.format(response_rooms_info))

        # go to main page
        self.setUp_main_page()
        self.setCurrentIndex(1)
