import socket
import struct
import binascii

host = socket.gethostbyname(socket.gethostname())

connection = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
connection.bind((host, 6672))

connection2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
connection2.bind((host, 61455))

while True:
    raw_data, address = connection.recvfrom(100)
    raw_data2, address2 = connection2.recvfrom(100)


    print(address,)
