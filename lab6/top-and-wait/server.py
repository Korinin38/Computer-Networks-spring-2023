import socket
from random import randint


address_to_server = ('localhost', 8888)
loss = 30

def troubled_sendto(self, thing, address):
    if randint(0, 99) >= loss:
        self.sendto(thing, address)



def pack(data_portion: bytes, index):
    return bytes([index]) + data_portion


def unpack(packet: bytes):
    return packet[0], packet[1:]


def try_recvfrom(self, index):
    while True:
        got, address = self.recvfrom(1024)
        print('Recieved, ', end='')
        got_index, got_data = unpack(got)
        print(got_index, 'vs', index, end='; ')
        if got_index != index:
            print('Unsuccessful.')
            print()
            troubled_sendto(self, pack('ACK'.encode('ascii'), index), address)
            continue

        print('Successful!')
        print()
        troubled_sendto(self, pack('ACK'.encode('ascii'), (index + 1) % 2), address)
        return got_data


def recv(self):
    to_ret = b''
    index = 0

    while True:
        got = try_recvfrom(self, index)
        if got == b'\0':
            break
        to_ret += got
        index = (index + 1) % 2

    return to_ret.decode('ascii')


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(address_to_server)
    print(f"Server is ready on {address_to_server[0]}, port {address_to_server[1]}")

    print(recv(server))
