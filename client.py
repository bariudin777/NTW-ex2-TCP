import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '192.168.43.43'
dest_port = 8000
s.connect((dest_ip, dest_port))
msg = input()
while not msg == 'quit':
    s.send(msg.encode())
    data = ""
    data = s.recv(4096)
    print(data.decode())
    msg = input()
s.close()
