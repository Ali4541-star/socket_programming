import socket
ip = "127.0.0.1"
port_sender = 9999
port_receiver = 9999

socket_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_receiver.bind((ip, port_receiver))
socket_receiver.listen(5)

socket_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_sender.connect((ip, port_receiver))

conn, addr = socket_receiver.accept()

i = 0
while i < 100:
    j = i * 2
    k = i * 5
    msg = str(i).encode("utf-8")
    socket_sender.send(msg)
    data = conn.recv(1024)
    print(data)
    i += 1