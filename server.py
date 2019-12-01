import socket
from re import search
import re

INSERT_PATTERN = "^1\s[\s0-9\s]*\s[a-zA-Z_.,-;]+$"
SEARCH_PATTERN = "^2\s[\s0-9\sa-zA-Z_.,-=)(]+$"

'''
Class Name: Handler
Args type: data, socket, set_val
Return Val: None
Info:
'''


class Handler:
    def __init__(self, data, socket, set_val):
        self.data = data
        self.socket = socket
        self.set_val = set_val

    '''
    Name:
    Args type: 
    Return Val:
    Info:
    '''

    def manage(self):

        if re.match(INSERT_PATTERN, self.data):
            self.set_val.process(self.data)
        if re.match(SEARCH_PATTERN, self.data):
            self.set_val.search(self.data, self.socket)


'''
Name:
Args type: 
Return Val:
Info:
'''


class Manager:

    def __init__(self, client_addr):
        self.dict = {}
        self.addr = client_addr

    '''
    Name:
    Args type: 
    Return Val:
    Info:
    '''

    def set(self, key, value):
        self.dict[key] = value

    '''
    Name:
    Args type: 
    Return Val:
    Info:
    '''

    def process(self, data):
        value = str(self.addr[0]) + " " + str(self.addr[1])
        to_split = data[7:]
        list_of_keys = str(to_split).split(",")
        for i in range(len(list_of_keys)):
            self.set(list_of_keys[i], value)

    '''
    Name:
    Args type: 
    Return Val:
    Info:
    '''

    def search(self, data, socket):
        if self.dict is None:
            print("There is no files")
        else:
            to_search = str(data[2:])
            msg = ""
            for i in self.dict:
                if to_search in i:
                    msg = msg + str(i) + " " + str(self.dict[i]) + " , "

            socket.send(msg[:len(msg) - 2].encode())


'''
Name:
Args type: 
Return Val:
Info:
'''
if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.43.43"
    server_port = 8000
    server.bind((server_ip, server_port))
    server.listen(5)

    while True:
        client_socket, client_address = server.accept()
        data = client_socket.recv(1024)
        set_val = Manager(client_address)
        while not data == "":
            handler = Handler(data.decode(), client_socket, set_val)
            handler.manage()
            client_socket.send(data.upper())  # to fix
            data = client_socket.recv(1024)

        print("Client Disconnected")
        client_socket.close()
