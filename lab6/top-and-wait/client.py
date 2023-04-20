import socket
from random import randint

address_to_server = ('localhost', 8888)
loss = 30

def data_split(data: bytes):
    batch_size = 1024
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


def troubled_sendto(self, thing, address):
    if randint(0, 99) >= loss:
        self.sendto(thing, address)


def pack(data_portion: bytes, index):
    return bytes([index]) + data_portion


def unpack(packet: bytes):
    return packet[0], packet[1:]


def try_sendto(self, thing, address, index):
    while True:
        try:
            troubled_sendto(self, pack(thing, index), address)

            ack, _ = self.recvfrom(1024)
            ack_index, ack_data = unpack(ack)
            print(ack_index, 'vs' , index)
            if ack_index != (index + 1) % 2 or ack_data.decode('ascii') != 'ACK':
                print('Invalid \'ACK\'')
                continue
            print('Transmission Successful!')
            break

        except socket.timeout:
            print('Nothing...')


def send(self, data, address):
    data = data_split(data.encode('ascii'))
    index = 0

    for batch in data:
        try_sendto(self, batch, address, index)
        index = (index + 1) % 2

    try_sendto(self, b'\0', address, index)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as client:
    client.settimeout(1.0)

    send(client, 'data: Hello World!', address_to_server)
