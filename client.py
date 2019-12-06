import socket
import sys
import os


def ready_to_upload(s,ip,port,port_to_listen):
    listen_ip = ip
    listen_port = port_to_listen
    s.bind((listen_ip, listen_port))
    s.listen(5)
    client_socket, client_address = s.accept()



def download(file_name):
    # open connection with the client how has the file
    # download the file from him,
    pass


def sendtoserver(msg):
    s.send(msg.encode())  # TODO - why it doesnt send anything?/?
    data = ""
    data = s.recv(4096)
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '10.0.0.2'
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
    data = sendtoserver('^' + msg)  # get the from server
    print(data.decode())
    file_to_download = s.recv(1024).decode()
    download(file_to_download)  # connect with the data


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
    ready_to_upload(s, sys.argv[2], sys.argv[3], sys.argv[4])


s.close()
