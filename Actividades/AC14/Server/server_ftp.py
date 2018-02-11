import os
import socket
import pickle


def send(conn, data):
    # Funcion para mandar comandos y archivos
    try:
        conn.send(pickle.dumps(data))
    except:
        print('Client invalid')


def receive(sock):
    # Funcion que recibe cualquier dato mandado por el servidor
    try:
        data = sock.recv(1024)
    except:
        return -1
    else:
        return pickle.loads(data)


def ls(path):
    return os.listdir(path)


def get_path(path):
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        return -1
    elif not os.path.isdir(abs_path):
        return 0
    else:
        return abs_path


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.sep.join(C_DIR.split(os.sep) +
                                           path.split(os.sep)))


if __name__ == '__main__':

    HOST = "localhost"
    PORT = 4003
    C_DIR = os.getcwd()
    print(C_DIR)

    client = None

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)

    print('Server started')

    while True:
        # Conectarse al servidor
        try:
            conn, addr = sock.accept()
            client = conn
            print('{} connected to server'.format(addr))

            # if connected send directory
            send(conn, C_DIR)
        except:
            connected = False
        else:
            connected = True

        while connected:
            # Recibir comandos
            try:
                message = receive(conn)
                action = message['command']
                args = message['args']
            except:
                action = ""

            if action == "ls":
                msg = ls(C_DIR)
                send(conn, msg)

            elif action == "logout":
                print('{} disconected from server'.format(addr))
                conn.close()
                client = None

            elif action == "get":
                filename = args
                msg = {'Found': False, 'Data': None}
                if filename in ls(C_DIR):
                    msg['Found'] = True
                    # set data to the file in bytes
                    with open(filename, 'rb') as f:
                        bytes_to_send = f.read()
                    msg['Data'] = bytes_to_send
                # send answer
                send(conn, msg)

            elif action == "send":
                new_name = args[1]
                serial = message['data']
                msg = {'Received': False}
                if new_name in ls(C_DIR):
                    msg['Received'] = False
                else:
                    with open(new_name, 'wb') as file:
                        file.write(serial)
                    msg['Received'] = True
                send(conn, msg)
