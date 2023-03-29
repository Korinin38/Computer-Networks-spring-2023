#!/usr/bin/env python3
import socket
import time
from datetime import datetime

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    server.settimeout(0.2)
    while True:
        message = str(datetime.now()).encode('ascii')
        server.sendto(message, ("255.255.255.255", 37020))
        print(f"{message} sent!", flush=True)
        time.sleep(1)