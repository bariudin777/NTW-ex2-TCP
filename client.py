import socket
import sys


def sendtoserver(msg):
    s.send(msg.encode())
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
    data = sendtoserver('^' + msg)

elif len(sys.argv) is 5:
    if sys.argv[1] is not '0':
        print("Wrong argument- if you want to listen, put '0' as the first arg")
        exit(0)
    msg = input()
    data = sendtoserver(msg)
    print(data.decode())
    listen_ip = sys.argv[2]
    listen_port = sys.argv[4]
    s.bind((listen_ip, listen_port))
    s.listen(5)
    client_socket, client_address = s.accept()
    data = client_socket.recv(1024)

s.close()
