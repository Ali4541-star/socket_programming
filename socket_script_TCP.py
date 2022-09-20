from sockets import TCPSocket

ip = "127.0.0.1"
port_sender = 9999
port_receiver = 9999


socket_receiver = TCPSocket(ip, port_receiver, True)
socket_sender = TCPSocket(ip, port_sender)
socket_receiver.connect()
socket_sender["i"] = 0
socket_sender["j"] = 0
socket_sender["k"] = 0

i = 0
while i < 100:
    j = i * 2
    k = i * 5
    socket_sender["i"] = i
    socket_sender["j"] = j
    socket_sender["k"] = k
    msg = str(i).encode("utf-8")
    socket_sender.send_msg(msg)
    received_message = socket_receiver.get_msg().decode("utf-8")
    print(f"received message is {received_message}")
    socket_sender.send_params()
    received_params = socket_receiver.get_msg().decode("utf-8")
    print(f"received parameters are {received_params}")
    i += 1
