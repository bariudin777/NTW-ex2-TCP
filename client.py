import json
from socket import *
import sys
import os


def checkmsg(message):
    # the input was just space or
    if not message:
        return False


def download(data):
    json_res = json.loads(data)
    ip = json_res["ip_port"][0]
    port = json_res["ip_port"][1]
    file_name = json_res["fileName"]
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip, port))
    s.send(file_name.encode())
    f = open(file_name, 'wb')
    load = s.recv(1024)
    while load:
        try:
            f.write(load)
            s.settimeout(1)
            load = s.recv(1024)
        except(timeout):
            break
    f.close()
    s.shutdown(SHUT_RD)
    # open connection with the client how has the file
    # download the file from him,


def sendtoserver(s, msg):
    try:
        s.send(msg.encode())  # TODO - why it doesnt send anything?/?
        data = ""
    except:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((dest_ip, dest_port))
        s.send(msg.encode())
    data = s.recv(4096)
    s.close()
    return data


s = socket(AF_INET, SOCK_STREAM)
dest_ip = '127.0.0.1'
dest_port = 8000
s.connect((dest_ip, dest_port))

# if there is 4 args- go to the user mode '1'
if len(sys.argv) is 4:
    if sys.argv[1] is not '1':
        print("Wrong argument- if you want to use, put '1' as the first arg")
        exit(0)
    while True:
        msg = input("Search: ")
        # check if the message is correct
        data = sendtoserver(s, '$' + msg)
        if checkmsg(data) is False:
            continue
        print(data.decode())
        msg = input("Choose: ")
        data = sendtoserver(s, '^' + msg)  # get the from server
        download(data.decode())  # connect with the data


elif len(sys.argv) is 5:
    if sys.argv[1] is not '0':
        print("Wrong argument- if you want to listen, put '0' as the first arg")
        exit(0)
    # msg = input()
    # data = sendtoserver(msg)
    # print(data.decode())
    data = os.listdir(".")
    data.append(sys.argv[4])
    s.send(('~' + ','.join(data)).encode())
    s.close()
    server = socket(AF_INET, SOCK_STREAM)
    server_ip = sys.argv[2]
    server_port = int(sys.argv[4])
    server.bind((server_ip, server_port))
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        file_name = client_socket.recv(1024).decode()
        f = open(file_name, 'rb')
        f.seek(0)
        payload = f.read(-1)
        while payload:
            client_socket.sendall(payload)
            payload = f.read(1024)
        f.close()
        server.shutdown(SHUT_WR)
