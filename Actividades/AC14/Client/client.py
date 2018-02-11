import os
import socket
import pickle


def send(sock, data):
    # Funcion para mandar comandos y archivos
    try:
        sock.send(pickle.dumps(data))
    except:
        print('Could not send from client')


def receive(sock):
    # Funcion que recibe cualquier dato mandado por el servidor
    try:
        data = sock.recv(1024)
    except:
        return -1
    else:
        return pickle.loads(data)


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

    C_DIR = os.getcwd()
    HOST = "localhost"
    PORT = 4003

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    sock.connect((HOST, PORT))

    S_DIR = receive(sock)

    print('Server found, S_DIR: {}'.format(S_DIR))

    connected = True

    while connected:
        command = input(S_DIR + " $ ")
        commands = command.split(" ")
        print(commands)

        if commands[0] == "logout":
            # Aviso al servidor que me desconecto
            print('Disconnected from server')
            connected = False
            msg = {'command': commands[0], 'args': None}
            send(sock, msg)

        elif commands[0] == "ls":
            # Muetra carpetas y archivos en el directorio del servidor

            # send request
            msg = {'command': commands[0], 'args': None}
            send(sock, msg)

            # receive answer
            data = receive(sock)
            print(data)

        elif commands[0] == "get":
            # Le pides un archivo al servidor
            # send request
            args = commands[1]
            msg = {'command': commands[0], 'args': args}
            my_filename = commands[2]
            send(sock, msg)

            # receive answer
            data = receive(sock)
            if not data['Found']:
                print('File not found')
            else:
                serial = data['Data']
                with open(my_filename, 'wb') as f:
                    f.write(serial)
                print('File received')

        elif commands[0] == "send":
            # le mandas un archivo al servidor
            args = commands[1:]
            file_path = get_abs_path(commands[1])
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    bytes_to_send = file.read()
                msg = {'command': commands[0], 'args': args, 'data': bytes_to_send}
                send(sock, msg)

                # receive answer
                data = receive(sock)
                if data['Received']:
                    print('File received by Server')
                else:
                    print('File was not received by Server')
            else:
                print(commands[1] + " doesn't exist.")
