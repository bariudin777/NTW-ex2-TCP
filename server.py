import socket
from re import search
import re

INSERT_PATTERN = "^1\s[\s0-9\s]*\s[a-zA-Z_.,-;]+$"
SEARCH_PATTERN = "^2\s[\s0-9\sa-zA-Z_.,-=)(]+$"


class Handler:
    def __init__(self, data, socket, set_val):
        self.data = data
        self.socket = socket
        self.set_val = set_val

    def manage(self):

        if re.match(INSERT_PATTERN, self.data):
            self.set_val.process(self.data)
        if re.match(SEARCH_PATTERN, self.data):
            self.set_val.search(self.data, self.socket)


class Manager:

    def __init__(self):
        self.dict = {}

    def set(self, key, value):
        self.dict[key] = value

    def process(self, data):
        value = data[2:6]
        to_split = data[7:]
        list_of_keys = str(to_split).split(",")
        for i in range(len(list_of_keys)):
            self.set(list_of_keys[i], value)

    def search(self, data, socket):
        if self.dict is None:
            print("There is no files")
        else:
            to_search = str(data[1:])
            for i in self.dict:
                if search(to_search, str(i)):  # TODO  - don't work!!!!!!
                    msg = str(i) + str(self.dict[i])
                    socket.send(msg)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "10.0.0.2"
    server_port = 8000
    server.bind((server_ip, server_port))
    server.listen(5)

    while True:
        client_socket, client_address = server.accept()
        print("Connection from: ", client_address)
        data = client_socket.recv(1024)
        set_val = Manager()
        while not data == "":
            handler = Handler(data.decode(), client_socket, set_val)
            handler.manage()
            client_socket.send(data.upper())
            data = client_socket.recv(1024)

        print("Client Disconnected")
        client_socket.close()
