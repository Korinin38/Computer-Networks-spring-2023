#!/usr/bin/env python3
import typing


def sum(data: bytearray) -> int:
    s = 0
    for i in range(0, len(data), 2):
        a = data[i]
        if i + 1 < len(data):
            b = data[i + 1]
        a <<= 16
        s += a + b
    return s


def check(data: bytearray, s: int) -> bool:
    res = sum(data) + ~s
    return not bool(~res)


def test(data):
    print("Test")
    print("data:", data)
    if type(data) is str:
        res = bytearray(data, 'utf-8')
    else:
        res = data
    print("sum:", sum(res))
    print("check:", check(res, sum(res)))
    print()


def antitest(data):
    print("Antitest")
    print("data:", data)
    if type(data) is str:
        res = bytearray(data, 'utf-8')
    else:
        res = data
    print("sum:", sum(res))

    res1 = res.copy()
    if len(res1) > 0:
        res1[-1] = res1[-1] + 1
    print("check:", check(res, sum(res1)))
    print()


if __name__ == "__main__":
    test("Hello World!")
    test("")
    test(bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8]))


    antitest("Hello World!")
    antitest("")
    antitest(bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8]))