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
        print("new connection from {address}".format(address=address))

        data = connection.recv(1024)
        print(str(data))
        if data == bytes("nslookup", encoding='UTF-8'):
            result = subprocess.check_output(["nslookup", "localhost"])
        elif data == bytes("ping", encoding='UTF-8'):
            result = subprocess.check_output(["ping", "yandex.ru", "-c", "4"])

        connection.send(result)

        connection.close()