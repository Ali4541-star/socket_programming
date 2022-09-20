import socket
import json
import base64

class UDPSocket(object):

    def __init__(self, ip, port, buffsize): # params eklenecek
        self.port = port
        self.buffsize = buffsize
        self.ip = ip
        self.max_buffsize = 65536
        self.__params = {}
        self.endpoint = None
        self.init_socket()


    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffsize)
        self.socket.bind((self.ip, self.port))
        print(f"Socket initialized to {self.port}")
        # print(f"Socket connected to IP:{self.endpoint[0]}, port:{self.endpoint}")

    def __delitem__(self, key):
        del self.__params[key]

    def __del__(self):
        print(f"Socket object with port {self.port} and ip {self.ip} is deleted")
        del self

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            try:
                key = str(key)
            except TypeError("Given key is not valid") as e:
                raise e
        self.__params[key] = value

    @property
    def mng_params(self): return self.__params

    @mng_params.setter
    def mng_params(self, keys):
        for key in keys:
            self.__params[key] = None

    @property
    def mng_buffsize(self): return self.buffsize

    @mng_buffsize.setter
    def mng_buffsize(self, size):
        if isinstance(size, int) and size >= 0 and size <= self.max_buffsize:
            self.buffsize = size

    def set_endpoint(self, ip:str, portnum:int):
        if not isinstance(ip, str) or not isinstance(portnum, int):
            raise Exception("Given variables are not compatible with endpoint")
        print(f"Endpoint is:{(ip, portnum)}")
        self.endpoint = (ip, portnum)
        print(f"Endpoint set to {ip}, {portnum}")

    def listen(self, show_address:bool=False):
        try:
            packet, address = self.socket.recvfrom(self.buffsize)
            if show_address:
                return packet, address
            else:
                return packet
        except socket.error as error:
            print("Message is not available", error)

    def send_msg(self, msg):
        assert self.endpoint is not None
        self.socket.sendto(msg, self.endpoint)

    def send_params(self):
        print(self.__params)
        encoded = json.dumps(self.__params, indent=4).encode("utf-8")
        print(f"Encoded is {encoded}")
        self.socket.sendto(encoded, self.endpoint)

class TCPSocket(object):

    max_portnum = 65535

    def __init__(self, ip, port, listen=False): # params eklenecek
        self.port = port
        self.ip = ip
        self.__params = {}
        self.endpoint = None
        self.init_socket(listen)

    def init_socket(self, listen):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if listen:
            self.socket.bind((self.ip, self.port))
            self.socket.listen()
        else:
            print(f"ip is {self.ip}, port is {self.port}")
            self.socket.connect((self.ip, self.port))
        print(f"Socket initialized to {self.port}")
        # print(f"Socket connected to IP:{self.endpoint[0]}, port:{self.endpoint}")

    def __delitem__(self, key):
        del self.__params[key]

    def __del__(self):
        print(f"Socket object with port {self.port} and ip {self.ip} is deleted")
        del self

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            try:
                key = str(key)
            except TypeError("Given key is not valid") as e:
                raise e
        self.__params[key] = value

    @property
    def mng_port(self): return self.port

    @mng_port.setter
    def mng_port(self, portnum):
        self.port = min(portnum, self.max_portnum)

    @property
    def mng_params(self): return self.__params

    @mng_params.setter
    def mng_params(self, keys):
        for key in keys:
            self.__params[key] = None

    def connect(self):
        print("Listening")
        self.conn, self.addr = self.socket.accept()
        print("listen started")

    def get_msg(self,  size=1024):
        return self.conn.recv(size)

    def send_msg(self, msg):
        self.socket.send(msg)

    def send_params(self):
        print(self.__params)
        encoded = json.dumps(self.__params).encode("utf-8")
        print(f"Encoded is {encoded}")
        self.socket.send(encoded)

    def close(self):
        self.socket.close()