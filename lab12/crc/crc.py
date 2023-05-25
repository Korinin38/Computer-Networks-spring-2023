#!/usr/bin/env python3
from itertools import islice

CRC_16 = 0x8005
CRC_16_CCITT = 0x1021
CRC_8_SAE = 0x1D

 
def chunk(arr, arr_size):
    arr = iter(arr)
    return iter(lambda: tuple(islice(arr, arr_size)), ())


def crc(bitchunk, poly, size):
    bin_num = int.from_bytes(bitchunk, "big")
    res = bin_num << size

    while res >= 1 << size:
        delimeter = (1 << size) + poly
        cont = 0
        while (1 << (cont + size + 1)) <= res:
            cont += 1
            # print("n:", bin(res))
            # print("i:", bin(1 << cont + size + 1))
        delimeter <<= cont
        print("a:", bin(res))
        print("b:", bin(delimeter))
        res ^= delimeter
        print("c:", bin(res))

    return res.to_bytes((size - 1) // 8 + 1, "big")


def crc_16(bitchunk):
    return crc(bitchunk, poly=CRC_16, size=16)

def crc_16_ccitt(bitchunk):
    return crc(bitchunk, poly=CRC_16_CCITT, size=16)


def crc_8(bitchunk):
    return crc(bitchunk, poly=CRC_8_SAE, size=8)


def crc_encrypt(text):
    print(f"Testing {text}")
    btext = text.encode(encoding="ASCII")
    for i in chunk(btext, 5):
        print(f'"{bytes(i).decode(encoding="ASCII")}": {i}')
        print(hex(int.from_bytes(crc_16_ccitt(i), "big")))
        

print(hex(int.from_bytes(crc_16_ccitt(b'\x01\x02'), "big")))
print(hex(int.from_bytes(crc_8(b'\xC2'), "big")))
crc_encrypt('Hello World!')
print(hex(int.from_bytes(crc_16_ccitt(str.encode('123456789', encoding="ASCII")), "big")))
crc_encrypt('Hi')
crc_encrypt('1')
