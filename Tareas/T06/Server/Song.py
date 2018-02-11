import os


class Song():

    def __init__(self, c_dir):
        aux = c_dir.split('/')
        self.genre = aux[2]
        self.filename = aux[3].replace('_', ' ')
        self.artist = self.filename.split('-')[0].strip()
        self.name = self.filename.split('-')[1].replace('.wav', '').strip()
        self.size = os.path.getsize(c_dir)

    def __repr__(self):
        return '{} - {}'.format(self.name, self.artist)
