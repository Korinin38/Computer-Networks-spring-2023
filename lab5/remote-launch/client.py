#!/usr/bin/env python3
import socket
address_to_server = ('localhost', 8888)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client: 
    client.connect(address_to_server)
    print("Client ready.\ntype 'nslookup' or 'ping' to start.")
    st = input()[:1024]

    client.send(bytes(st, encoding='UTF-8'))
    data = client.recv(1024)
    print(data.decode('UTF-8'))
