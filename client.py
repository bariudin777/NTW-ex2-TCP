import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '10.0.0.2'
dest_port = 8000
s.connect((dest_ip, dest_port))
msg = input("Message to send: ")
while not msg == 'quit':
    s.send(msg.encode())
    data = s.recv(4096)
    print("Server sent: ", data)
    msg = input("Message to send:")
s.close()