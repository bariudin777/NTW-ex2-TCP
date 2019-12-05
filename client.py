import socket
import sys
import os


def download(file_name):
    pass


def sendtoserver(msg):
    s.send(msg.encode())
    data = ""
    data = s.recv(4096)
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '172.18.21.23'
dest_port = 8000
s.connect((dest_ip, dest_port))

# if there is 4 args- go to the user mode '1'
if len(sys.argv) is 4:
    if sys.argv[1] is not '1':
        print("Wrong argument- if you want to use, put '1' as the first arg")
        exit(0)
    msg = input("Search: ")
    data = sendtoserver('$' + msg)
    print(data.decode())
    msg = input("Choose: ")
    data = sendtoserver('^' + msg)
    file_to_download = s.recv(1024).decode()
    download(file_to_download)


elif len(sys.argv) is 5:
    if sys.argv[1] is not '0':
        print("Wrong argument- if you want to listen, put '0' as the first arg")
        exit(0)
    # msg = input()
    # data = sendtoserver(msg)
    # print(data.decode())
    data = os.listdir(".")
    s.send((str('~' + str(data)).encode()))
    #    listen_ip = sys.argv[2]
    #    listen_port = sys.argv[4]
    listen_ip = "172.18.21.23"
    listen_port = 9000
    s.bind((listen_ip, listen_port))
    s.listen(5)
    client_socket, client_address = s.accept()

s.close()
