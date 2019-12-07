import json
import os
import socket
import sys
from re import search
from socket import *
import re

INSERT_PATTERN = "[~a-zA-Z_.,-;]+"  # TODO fix the regex!!!
SEARCH_PATTERN = "^2\s[\s0-9\sa-zA-Z_.,-=)(]+$"  # TODO fix the regex!!!
USER_SEARCH = "^\$[\s0-9\sa-zA-Z_.,-=)(]+$"
CHOOSE_PATTERN = "^\^[\s0-9\sa-zA-Z_.,-=)(]+$"
'''
Class Name: Handler
Args type: data, socket, set_val
Return Val: None
Info: Handel's Clients data
'''


# pinuspunanos

class Handler:
    def __init__(self, data, socket, set_val):
        self.data = data
        self.socket = socket
        self.set_val = set_val

    '''
    Name: manage 
    Args type: None
    Return Val: None
    Info: Manage client's input- registration and search 
    '''

    def manage(self):
        # File registration
        if re.match(INSERT_PATTERN, self.data):
            self.set_val.process(self.data[1:])
        # File search
        if re.match(SEARCH_PATTERN, self.data):
            self.set_val.search(self.data[2:], self.socket)
        # User search
        if re.match(USER_SEARCH, self.data):
            self.set_val.search(self.data[1:], self.socket)
        # User choose
        if re.match(CHOOSE_PATTERN, self.data):
            self.set_val.choose(self.data[1:], self.socket)


'''
Class Name: Manager - ּStatic Class- Singleton
Args type: Client address
Return Val: None
Info: Manage Clients Info- what files he posses
'''


class Manager:
    __instance = None

    @staticmethod
    def getInstance(client_address):
        if Manager.__instance is None:
            Manager(client_address)
        return Manager.__instance

    def __init__(self, client_addr):
        if Manager.__instance is not None:
            raise Exception("This class is singleton! ")
        else:
            Manager.__instance = self
            self.dict = {}
            self.addr = client_addr
            self.indexeddata = {}

    '''
    Name: set
    Args type: key, value
    Return Val: None
    Info: Sets the dictionary
    '''

    def set(self, key, value):
        self.dict[key] = value

    '''
    Name: process
    Args type: data
    Return Val: None
    Info: Split and Parse the data for the dictionary
    '''

    def process(self, data):

        value = self.addr
        for file in data.split(','):
            self.set(file, value)

    '''
    Name: search
    Args type: data , socket
    Return Val: None
    Info: Searches files name or sub-string of files name and send it 
    '''

    def search(self, data, socket):
        if self.dict is None:
            print("The word: " + str(data) + " don't exists - there is no such file name ")
        else:
            msg = ""
            counter = 1
            # sorts the massages to the client
            self.indexeddata = {}
            for k in sorted(self.dict.keys()):
                if data in k:
                    self.indexeddata[counter] = k
                    msg += str(counter) + " " + str(k) + "\n"
                    counter += 1
            socket.send(msg[:len(msg) - 1].encode())

    def choose(self, data, socket):
        ip_port = self.dict[self.indexeddata[int(data)]]
        file_name = self.indexeddata[int(data)]
        res = {"ip_port": ip_port,
               "fileName": file_name}
        json_res = json.dumps(res)
        socket.send(json_res.encode())


'''
Name: Main
Args type:
Return Val:
Info:
'''
if __name__ == "__main__":

    server = socket(AF_INET, SOCK_STREAM)
    server_ip = "10.0.0.2"
    server_port = 8000
    server.bind((server_ip, server_port))
    server.listen(5)

    while True:
        client_socket, client_address = server.accept()
        data = client_socket.recv(1024)
        data = data.decode()
        if data[0] is '~':
            list_port = data[1:len(data)].split(",").pop()
            ip_to_set = (client_address[0], int(list_port))
        else:
            ip_to_set = client_address
        set_val = Manager.getInstance(ip_to_set)
        handler = Handler(data, client_socket, set_val)
        handler.manage()
        client_socket.close()
