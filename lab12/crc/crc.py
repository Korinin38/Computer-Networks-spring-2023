#!/usr/bin/env python3
from itertools import islice
from random import randint, sample

CRC_16 = 0x8005
CRC_16_CCITT = 0x1021
CRC_8_SAE = 0x1D


def chunk(arr, arr_size):
    arr = iter(arr)
    return iter(lambda: tuple(islice(arr, arr_size)), ())


def crc_check(bitchunk, poly=CRC_16_CCITT, size=16):
    res = crc(bitchunk, poly, size)
    return True if int.from_bytes(res, "big") == 0 else False


def crc_check_16_ccitt(bitchunk):
    return crc_check(bitchunk, poly=CRC_16_CCITT, size=16)


def crc(bitchunk, poly=CRC_16_CCITT, size=16):
    bin_num = int.from_bytes(bitchunk, "big")
    res = bin_num << size

    while res >= 1 << size:
        delimeter = (1 << size) + poly
        cont = 0
        while (1 << (cont + size + 1)) <= res:
            cont += 1
        delimeter <<= cont
        res ^= delimeter

    return res.to_bytes((size - 1) // 8 + 1, "big")


# def crc_16(bitchunk):
#     return crc(bitchunk, poly=CRC_16, size=16)


def crc_16_ccitt(bitchunk):
    return crc(bitchunk, poly=CRC_16_CCITT, size=16)


# def crc_8(bitchunk):
#     return crc(bitchunk, poly=CRC_8_SAE, size=8)


def crc_encrypt(text):
    btext = text.encode(encoding="ASCII")
    res = bytearray()
    for i in chunk(btext, 5):
        res.extend(bytes(i))
        res.extend(crc(i))
    return res


def crc_decrypt(bytes):
    err = False
    s = ""
    crcs = []
    for i in chunk(bytes, 7):
        res = crc_check(i)
        if res:
            s += bytearray(i[:-2]).decode(encoding="ASCII")
            crcs.append(bytearray(i[-2:]))
        else:
            print("Error!")
            err = True
    return s, crcs, err


byte_123 = str.encode('123456789', encoding="ASCII")


def corrupt(bytechunk, count=2):
    if len(bytechunk) - 2 < count:
        count = len(bytechunk) - 2
    for i in sample(range(len(bytechunk) - 2), count):
        bytechunk[i] ^= 1 << randint(0, 7)


def test_correct(str):
    print(f"---------------\nTesting correct {str}")
    coded = crc_encrypt(str)
    decoded, crcs, err = crc_decrypt(coded)
    print("\nResults:")
    print(decoded)
    for c in crcs:
        print(hex(int.from_bytes(c, "big")))
    if err:
        print("\nTest failed.\n")
    else:
        print("\nTest passed.\n")
    return not err


def test_corrupt(str):
    print(f"---------------\nTesting corrupt {str}")
    coded = crc_encrypt(str)
    corrupt(coded)
    decoded, crcs, err = crc_decrypt(coded)
    print("\nResults:")
    print(decoded)
    for c in crcs:
        print(hex(int.from_bytes(c, "big")))
    if not err:
        print("\nTest failed.\n")
    else:
        print("\nTest passed.\n")
    return err


if __name__ == "__main__":
    test_cases = ["123456789", "Hello World!", "1"]
    assert all(test_correct(t) for t in test_cases)
    assert all(test_corrupt(t) for t in test_cases)
