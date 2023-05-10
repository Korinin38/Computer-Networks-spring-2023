#!/usr/bin/env python3
import socket
import subprocess
address_to_server = ('localhost', 8888)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(address_to_server)
    server.listen(10)
    
    print(f"Server is ready on {address_to_server[0]}, port {address_to_server[1]}")

    while True:
        connection, address = server.accept()
        print("Connected to client {address}".format(address=address))

        while True:
            data = connection.recv(1024)
            print(str(data))
