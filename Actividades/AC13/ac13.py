import os
from datetime import datetime
import json
import pickle


# make dirs
try:
    os.mkdir('secure_db')
    os.mkdir('secure_db/usr')
    os.mkdir('secure_db/msg')
except FileExistsError:
    print('File already exists c:')


class User:

    def __init__(self, name, phone_number, contacts=None):
        self.name = name
        if contacts is None:
            self.contacts = []
        else:
            self.contacts = contacts
        self.phone_number = phone_number

    @classmethod
    def from_dict(cls, d):
        name = d['name']
        phone_number = int(d['phone_number'])
        contacts = []
        return cls(name, phone_number, contacts)


class Message:

    def __init__(self, send_to, content, send_by, date):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.date = date
        self.last_view_date = ""

    @classmethod
    def from_dict(cls, d):
        send_to = int(d['send_to'])
        content = d['content']
        send_by = int(d['send_by'])
        date = d['date']
        return cls(send_to, content, send_by, date)

    def __getstate__(self):
        # Serialization
        nueva = self.__dict__.copy()
        nueva.update({"content": encriptar(self.content, self.send_by)})
        return nueva

    def __setstate__(self, state):
        state.update({'last_view_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        self.__dict__ = state


def load_msgs():
    # returns a list with messages
    files = os.listdir('./db/msg')
    loaded = []
    for f in files:
        with open('db/msg/{}'.format(f)) as file:
            d = json.loads(next(file))
        loaded.append(Message.from_dict(d))

    return loaded


def load_users():
    # returns a list with users
    files = os.listdir('./db/usr')
    loaded = []
    for f in files:
        with open('db/usr/{}'.format(f)) as file:
            d = json.loads(next(file))
        loaded.append(User.from_dict(d))

    return loaded


def load_contacts(msgs, users):
    # returns a new users list with contacts
    for msg in msgs:
        origin_number = msg.send_by
        destination_number = msg.send_to
        origin = [i for i in users if i.phone_number == origin_number].pop()
        origin.contacts.append(destination_number)

    return users


def save_users(users):
    try:
        os.mkdir('secure_db/usr')
    except FileExistsError:
        print('File already exists')

    for user in users:
        with open('secure_db/usr/{}'.format(user.phone_number), 'w') as file:
            json.dump(user.__dict__, file)


def encriptar(string, n):
    # returns the string encrypted
    alphabet = [chr(i) for i in range(97, 123)]
    new = ""
    for c in string:
        if c not in alphabet:
            new += c
        else:
            number = ((ord(c) - 97 + n) % 26) + 97
            new += chr(number)

    return new


def save_msgs(msgs):
    try:
        os.mkdir('secure_db/msg')
    except FileExistsError:
        print('File already exists')

    for msg in msgs:
        with open('secure_db/msg/{}'.format(msg.send_by), 'bw') as file:
            pickle.dump(msg, file)


msgs = load_msgs()
users = load_users()
new_users = load_contacts(msgs, users)


# save users
save_users(new_users)

# save msgs
save_msgs(msgs)

# check if de serialization is correct
with open('secure_db/msg/45348826', 'rb') as file:
    msg_1 = pickle.load(file)
    print(msg_1.__dict__)
