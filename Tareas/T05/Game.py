from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem, QGraphicsLineItem)
import sys
from random import choice
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPen

# sound
from PyQt5 import QtMultimedia as M
from Tower import Tower
from Button import MenuButton, GameButton, ChampionButton
from StoreIcon import StoreIcon
from Nexus import Nexus
from Inhibitor import Inhibitor
from Minion import Minion
from BigMinion import BigMinion
from PlayerChampion import PlayerMage, PlayerTroll, PlayerOgrillion
from ComputerChampion import ComputerMage, ComputerTroll, ComputerOgrillion
from Score import Score


class Game(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('League of Progra')
        self.on_game = False
        self.player = None
        self.champion_election = None

        # to detect mouse movement
        self.setMouseTracking(True)
        # create a scene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1024, 700)

        # set scene
        self.setScene(self.scene)

        self.setFixedSize(1024, 700)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # background menu music
        self.playlist_1 = M.QMediaPlaylist()
        self.playlist_1.addMedia(M.QMediaContent(QUrl('./res/music/intro.ogg')))
        self.playlist_1.setPlaybackMode(M.QMediaPlaylist.Loop)
        self.menu_music = M.QMediaPlayer()
        self.menu_music.setPlaylist(self.playlist_1)
        self.menu_music.setVolume(20)

        # background in game music
        self.playlist_2 = M.QMediaPlaylist()
        self.playlist_2.addMedia(M.QMediaContent(QUrl('./res/music/BattleTheme-hugoleo777.ogg')))
        self.playlist_2.setPlaybackMode(M.QMediaPlaylist.Loop)
        self.in_game_music = M.QMediaPlayer()
        self.in_game_music.setPlaylist(self.playlist_2)
        self.in_game_music.setVolume(20)

        #
        self.get_player_waiting_time = self.get_champion_waiting_time()
        self.get_enemy_waiting_time = self.get_champion_waiting_time()

    def start(self):
        # clear the screen
        self.scene.clear()
        self.on_game = True

        # play background in game music
        if self.menu_music.state() == M.QMediaPlayer.PlayingState:
            self.menu_music.stop()

        self.in_game_music.play()

        # draw gui buttons
        self.draw_GUI()

        # set background
        self.scene.setBackgroundBrush(QBrush(QImage('./res/imgs/grass_background.jpg')))

        # create towers
        self.t_1 = Tower()
        self.t_1.setPos(580, 400)

        self.t_2 = Tower()
        self.t_2.setPos(350, 240)
        self.t_2.set_team(2)

        # create nexus
        self.n_1 = Nexus()
        self.n_1.setPos(900, 615)

        self.n_2 = Nexus()
        self.n_2.setPos(30, 20)
        self.n_2.set_team(2)

        self.n_1.s.died.connect(self.game_over)
        self.n_2.s.died.connect(self.game_over)

        # create inhibitor
        self.i_1 = Inhibitor()
        self.i_1.setPos(740, 505)

        self.i_2 = Inhibitor()
        self.i_2.setPos(190, 130)
        self.i_2.set_team(2)

        self.i_1.s.died.connect(self.inhibitor_died)
        self.i_2.s.died.connect(self.inhibitor_died)

        # initialize bool to check if inhibitor is alive
        self.inhibitor_1_alive = True
        self.inhibitor_2_alive = True

        # add everything to scene
        self.scene.addItem(self.t_1)
        self.scene.addItem(self.n_1)
        self.scene.addItem(self.i_1)

        self.scene.addItem(self.t_2)
        self.scene.addItem(self.n_2)
        self.scene.addItem(self.i_2)

        # initialize spawn of unitary minions
        self.spawn_timer_1 = QTimer()
        self.spawn_timer_2 = QTimer()

        # initialize spawn of 5 minions per team
        self.big_spawn_1 = QTimer()
        self.big_spawn_2 = QTimer()
        self.big_spawn_1.timeout.connect(lambda: self.create_allies(5))
        self.big_spawn_2.timeout.connect(lambda: self.create_enemies(5))
        self.big_spawn_1.start(40000)
        self.big_spawn_2.start(40000)

        # add champion to scene
        self.spawn_player()

        # add enemy champion
        self.enemy_name = choice(['Mage', 'Ogrillion', 'Troll'])
        self.spawn_enemy()

    def spawn_player(self):
        if self.player_name == 'Mage':
            self.player = PlayerMage()
        elif self.player_name == 'Troll':
            self.player = PlayerTroll()
        elif self.player_name == 'Ogrillion':
            self.player = PlayerOgrillion()
        self.player.set_team(1)
        self.player.s.died.connect(self.champion_died)
        self.player.setPos(800, 600)
        self.player.setFlag(QGraphicsItem.ItemIsFocusable)
        self.player.setFocus()
        self.scene.addItem(self.player)

    def spawn_enemy(self):
        if self.enemy_name == 'Mage':
            self.enemy = ComputerMage()
        elif self.enemy_name == 'Troll':
            self.enemy = ComputerTroll()
        elif self.enemy_name == 'Ogrillion':
            self.enemy = ComputerOgrillion()
        self.enemy.set_team(2)
        self.enemy.s.died.connect(self.champion_died)
        self.enemy.setPos(80, 300)
        self.scene.addItem(self.enemy)
        # set store not available
        self.store.set_available(False)
        self.store.timer.start(1000)

    def champion_died(self):
        champion_signal = self.sender()
        if champion_signal == self.player.s:
            self.player = None
            self.store.timer.stop()
            self.store.set_available(True)
            self.spawn_player_timer = QTimer()
            self.spawn_player_timer.timeout.connect(self.spawn_player)
            self.spawn_player_timer.setSingleShot(True)
            self.spawn_player_timer.start(next(self.get_player_waiting_time))

        elif champion_signal == self.enemy.s:
            self.spawn_enemy_timer = QTimer()
            self.spawn_enemy_timer.timeout.connect(self.spawn_enemy)
            self.spawn_enemy_timer.setSingleShot(True)
            self.spawn_enemy_timer.start(next(self.get_enemy_waiting_time))

    def inhibitor_died(self):
        WAITING_TIME = 30000
        inhibitor_sender = self.sender()
        if inhibitor_sender == self.i_1.s:
            self.inhibitor_1_alive = False
            self.n_1.set_damageable(True)
            self.rec_timer_1 = QTimer()
            self.rec_timer_1.timeout.connect(self.rec_inhibitor_1)
            self.rec_timer_1.setSingleShot(True)
            self.rec_timer_1.start(WAITING_TIME)
        elif inhibitor_sender == self.i_2.s:
            self.inhibitor_2_alive = False
            self.n_2.set_damageable(True)
            self.rec_timer_2 = QTimer()
            self.rec_timer_2.timeout.connect(self.rec_inhibitor_2)
            self.rec_timer_2.setSingleShot(True)
            self.rec_timer_2.start(WAITING_TIME)

    def rec_inhibitor_1(self):
        # create inhibitor, pos, add to scene, set nexus damageable = False
        self.i_1 = Inhibitor()
        self.i_1.setPos(740, 505)
        self.i_1.set_team(1)
        self.i_1.s.died.connect(self.inhibitor_died)
        self.scene.addItem(self.i_1)

        self.n_1.set_damageable(False)

    def rec_inhibitor_2(self):
        # create inhibitor, pos, add to scene, set nexus damageable = False
        self.i_2 = Inhibitor()
        self.i_2.setPos(190, 130)
        self.i_2.set_team(2)
        self.i_2.s.died.connect(self.inhibitor_died)
        self.scene.addItem(self.i_2)

        self.n_2.set_damageable(False)

    def mouseMoveEvent(self, event):
        if self.on_game and self.player:
            if not self.player.move_timer.isActive():
                self.player.rotate_to_point(event.pos())
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.on_game:
            if event.button() == Qt.RightButton:
                if self.player.ulti_available:
                    self.player.ulti()

            elif event.button() == Qt.LeftButton:
                selected_items = self.scene.items(event.pos())
                for i in selected_items:
                    if hasattr(i, 'team') and i.team == 2:
                        self.player.simple_attack(i)
                        break
        if self.player:
            self.player.setFocus()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if self.on_game:
            if event.key() == Qt.Key_P:
                self.pause()
            elif event.key() == Qt.Key_O:
                print('Not implemented')
            elif event.key() == Qt.Key_I:
                self.display_main_menu()
        super().keyPressEvent(event)

    def create_allies(self, number_of_allies):
        self.allies_spawned = 0
        self.max_number_of_allies = number_of_allies
        self.spawn_timer_1.timeout.connect(self.spawn_ally_minions)
        self.spawn_timer_1.start(1000)

    def spawn_ally_minions(self):
        if self.allies_spawned >= self.max_number_of_allies:
            self.spawn_timer_1.disconnect()
        else:
            if self.allies_spawned == 4:
                minion = BigMinion(powered_up=not self.inhibitor_1_alive)
            else:
                minion = Minion()

            minion.set_team(1)
            minion.setPos(850, 500)
            self.scene.addItem(minion)
            self.allies_spawned += 1

    def create_enemies(self, number_of_enemies):
        self.enemies_spawned = 0
        self.max_number_of_enemies = number_of_enemies
        self.spawn_timer_2.timeout.connect(self.spawn_enemy_minions)
        self.spawn_timer_2.start(1000)

    def spawn_enemy_minions(self):
        if self.enemies_spawned >= self.max_number_of_allies:
            self.spawn_timer_2.disconnect()
        else:
            if self.enemies_spawned == 4:
                minion = BigMinion(powered_up=not self.inhibitor_2_alive)
            else:
                minion = Minion()

            minion.set_team(2)
            minion.setPos(20, 120)
            self.scene.addItem(minion)
            self.enemies_spawned += 1

    def display_main_menu(self):
        # clear the scene
        self.player = None
        self.enemy = None
        self.scene.clear()
        self.on_game = False
        self.scene.setBackgroundBrush(QBrush())

        # play music
        if self.in_game_music.state() == M.QMediaPlayer.PlayingState:
            self.in_game_music.stop()

        self.menu_music.play()

        # create the title text
        self.title_text = QGraphicsTextItem('League of Progra')
        title_font = QFont('comic sans', 50)
        self.title_text.setFont(title_font)
        t_x_pos = self.width() / 2 - self.title_text.boundingRect().width() / 2
        t_y_pos = 150
        self.title_text.setPos(t_x_pos, t_y_pos)
        self.scene.addItem(self.title_text)

        # create play button
        self.play_btn = MenuButton('Play')
        b_x_pos = self.width() / 2 - self.play_btn.boundingRect().width() / 2
        b_y_pos = 275
        self.play_btn.setPos(b_x_pos, b_y_pos)
        self.play_btn.s.clicked.connect(self.display_selection_menu)
        self.scene.addItem(self.play_btn)

        # create Delete Save Games
        self.del_games_btn = MenuButton('Delete Save Games')
        db_x_pos = self.width() / 2 - self.del_games_btn.boundingRect().width() / 2
        db_y_pos = 350
        self.del_games_btn.setPos(db_x_pos, db_y_pos)
        self.del_games_btn.s.clicked.connect(lambda: print('Not implemented'))
        self.scene.addItem(self.del_games_btn)

        # create the quit btn
        self.quit_btn = MenuButton('Quit')
        qb_x_pos = self.width() / 2 - self.quit_btn.boundingRect().width() / 2
        qb_y_pos = 425
        self.quit_btn.setPos(qb_x_pos, qb_y_pos)
        self.quit_btn.s.clicked.connect(self.close)
        self.scene.addItem(self.quit_btn)

    def draw_GUI(self):
        # draw the menu button
        self.menu_btn = GameButton('Go to Menu')
        menu_btn_x = self.width() - 2 * self.menu_btn.rect().width()
        menu_btn_y = 0
        self.menu_btn.setPos(menu_btn_x, menu_btn_y)
        self.menu_btn.s.clicked.connect(self.display_main_menu)
        self.scene.addItem(self.menu_btn)

        # draw the pause button
        self.pause_btn = GameButton('Pause')
        pause_btn_x = self.width() - self.pause_btn.rect().width()
        pause_btn_y = 0
        self.pause_btn.setPos(pause_btn_x, pause_btn_y)
        self.pause_btn.s.clicked.connect(self.pause)
        self.scene.addItem(self.pause_btn)

        # draw the store
        self.store = StoreIcon()
        self.store.setPos(900, 500)
        self.scene.addItem(self.store)

        # draw the score
        self.score = Score()
        self.score.setPos(0, self.height() - self.score.boundingRect().height())
        self.scene.addItem(self.score)

    def display_selection_menu(self):
        # clear the scene
        self.scene.clear()
        self.on_game = False

        # create the title text
        self.title_text = QGraphicsTextItem('It is YOUR turn to PICK')
        title_font = QFont('comic sans', 30)
        self.title_text.setFont(title_font)
        t_x_pos = self.width() / 2 - self.title_text.boundingRect().width() / 2
        t_y_pos = 150
        self.title_text.setPos(t_x_pos, t_y_pos)
        self.scene.addItem(self.title_text)

        # draw panel behind buttons
        self.draw_panel(180, 200, 0.7 * self.width(), 100, Qt.lightGray,
                        0.75)

        # champions buttons (3)
        self.c_btn_1 = ChampionButton('Amumu')
        self.c_btn_2 = ChampionButton('Annie')
        self.c_btn_3 = ChampionButton('Olaf')

        # show buttons to scene
        self.c_btn_1.setPos(200, 225)
        self.c_btn_2.setPos(245, 225)
        self.c_btn_3.setPos(290, 225)

        self.scene.addItem(self.c_btn_1)
        self.scene.addItem(self.c_btn_2)
        self.scene.addItem(self.c_btn_3)

        # connect buttons to pick_champion function
        self.c_btn_1.s.clicked.connect(self.pick_champion)
        self.c_btn_2.s.clicked.connect(self.pick_champion)
        self.c_btn_3.s.clicked.connect(self.pick_champion)

        # lock in button
        self.lock_in_btn = MenuButton('Lock in')
        self.lock_in_btn.lock()
        lock_in_btn_x = self.width() / 2 - self.lock_in_btn.boundingRect().width() / 2
        lock_in_btn_y = 350
        self.lock_in_btn.setPos(lock_in_btn_x, lock_in_btn_y)
        self.lock_in_btn.s.clicked.connect(self.start)
        self.scene.addItem(self.lock_in_btn)

    def pick_champion(self):
        btn = self.sender()
        if btn == self.c_btn_1.s:
            self.player_name = 'Mage'
        elif btn == self.c_btn_2.s:
            self.player_name = 'Ogrillion'
        elif btn == self.c_btn_3.s:
            self.player_name = 'Troll'

        self.lock_in_btn.unlock()

    def pause(self, call_display_pause_screen=True):
        # stop all the timers
        self.big_spawn_1.stop()
        self.big_spawn_2.stop()

        scene_items = self.scene.items()
        self.items_freezed = []
        for i in scene_items:
            if hasattr(i, 'move_timer') and i.move_timer.isActive():
                i.move_timer.stop()
                self.items_freezed.append(i)
            if hasattr(i, 'damage_timer') and i.damage_timer.isActive():
                i.damage_timer.stop()
                self.items_freezed.append(i)
            if hasattr(i, 'wasd_timer') and i.wasd_timer.isActive():
                i.wasd_timer.stop()
                self.items_freezed.append(i)
            if hasattr(i, 'execute_ulti_timer') and i.execute_ulti_timer.isActive():
                i.execute_ulti_timer.stop()
                self.items_freezed.append(i)

        # call display pause window (with an unpause btn)
        if call_display_pause_screen:
            self.display_pause_screen()

    def unpause(self):
        # restart all timers and enable items
        for i in self.scene.items():
            i.setEnabled(True)

        self.big_spawn_1.start(20000)
        self.big_spawn_2.start(20000)

        for i in self.items_freezed:
            if hasattr(i, 'move_timer'):
                i.move_timer.start(1000 / 30)
            if hasattr(i, 'damage_timer'):
                i.damage_timer.start(1000)
            if hasattr(i, 'wasd_timer'):
                i.wasd_timer.start(1000 / 30)
            if hasattr(i, 'execute_ulti_timer'):
                i.execute_ulti_timer.start(10000)

        self.scene.removeItem(self.resume)
        self.scene.removeItem(self.paused_text)

        del self.items_freezed

    def display_pause_screen(self):
        # disable everything
        for i in self.scene.items():
            i.setEnabled(False)

        # create resume btn
        self.resume = MenuButton('Resume')
        self.resume.setPos(410, 300)
        self.scene.addItem(self.resume)
        self.resume.s.clicked.connect(self.unpause)

        # a nice text
        self.paused_text = QGraphicsTextItem('Paused')
        font = QFont('comic sans', 20)
        self.paused_text.setFont(font)
        self.paused_text.setPos(460, 225)
        self.scene.addItem(self.paused_text)

    def game_over(self):
        # function to be connected with the nexus
        # call game_over_window with a message

        # check who nexus sent the signal
        nexus_signal = self.sender()
        if nexus_signal == self.n_1.s:
            message = 'Defeated'
        elif nexus_signal == self.n_2.s:
            message = 'Victory'

        # call display game over
        self.display_game_over_window(message)

    def display_game_over_window(self, message):
        # disable all scene item
        for i in self.scene.items():
            i.setEnabled(False)

        # pause everithing but do not display the pause screen
        self.pause(call_display_pause_screen=False)

        # make the background dark
        self.draw_panel(0, 0, self.width(), self.height(),
                        Qt.black, 0.65)

        # draw panel
        self.draw_panel(312, 184, 400, 400, Qt.lightGray, 0.75)

        # create playAgain btn
        self.play_again = MenuButton('Play Again')
        self.play_again.setPos(410, 300)
        self.scene.addItem(self.play_again)
        self.play_again.s.clicked.connect(self.restart)

        # create quit button
        self.quit = MenuButton('Quit')
        self.quit.setPos(410, 375)
        self.scene.addItem(self.quit)
        self.quit.s.clicked.connect(self.close)

        # create text announcing winner
        self.over_text = QGraphicsTextItem(message)
        self.over_text.setPos(460, 225)
        self.scene.addItem(self.over_text)

    def restart(self):
        # clear everything
        self.scene.clear()

        # call start function
        self.display_selection_menu()

    def draw_panel(self, x, y, width, height, color, opacity):
        '''int x, int y, int, width, int height, QColor color, float opacity '''
        panel = QGraphicsRectItem(x, y, width, height)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(color)
        panel.setBrush(brush)
        panel.setOpacity(opacity)
        self.scene.addItem(panel)

    @staticmethod
    def get_champion_waiting_time():
        BASE_TIME = 10000
        i = 0
        while True:
            yield 1.1**i * BASE_TIME
            i += 1
