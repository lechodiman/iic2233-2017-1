import os
from Song import Song


class Room:

    def __init__(self, genre):
        self.genre = genre

        # initialize songs list
        self.songs = list()
        self.load_songs()

        # users in this room
        self.clients_here = list()

    def load_songs(self):
        '''Loads songs from directory '''
        songs = os.listdir('./Canciones/{}'.format(self.genre))
        for sname in songs:
            s = Song('./Canciones/{}/{}'.format(self.genre, sname))
            self.songs.append(s)

    def get_songs_info(self):
        list_to_return = [{'name': s.name,
                           'artist': s.artist,
                           'genre': s.genre} for s in self.songs]
        return list_to_return

    def get_songs_names(self):
        return [repr(s) for s in self.songs]
