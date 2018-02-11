
class User:
    def __init__(self, username='', points=int(),
                 points_per_room=dict()):
        self.username = username
        self.points = points
        self.points_per_room = points_per_room

    def get_points(self):
        return self.points

    def increase_points(self, value):
        self.points += value

    def set_username(self, name):
        self.username = name

    def get_username(self):
        return self.username

    @classmethod
    def from_dict(cls, user_dict):
        username = user_dict['username']
        points = user_dict['points']
        points_per_room = user_dict['points_per_room']

        return cls(username, points, points_per_room)
