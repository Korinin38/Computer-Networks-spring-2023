#!/usr/bin/env python3
import socket
import tkinter
import threading
import queue

address_to_server = ('localhost', 8888)
canvas_width = 450
canvas_height = 450

the_queue = queue.Queue()

def paint(x, y):
    color = 'red'
    x1, y1 = (x - 1), (y - 1)
    x2, y2 = x1 + 2, y1 + 2
    c.create_oval(x1, y1, x2, y2, fill=color, outline=color)


def recieve():
    while True:
        data = connection.recv(1024)
        x = data[0] * 256 + data[1]
        y = data[2] * 256 + data[3]
        the_queue.put((x, y))


def after_callback():
    while True:
        try:
            message = the_queue.get(block=False)
        except queue.Empty:
            # let's try again later
            master.after(20, after_callback)
            return
        
        if message is not None:
            paint(*message)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address_to_server)
    server.listen(10)

    print(f"Server is ready on {address_to_server[0]}, port {address_to_server[1]}")

    connection, address = server.accept()
    print("Connected to client {address}".format(address=address))


    master = tkinter.Tk()
    master.title('Remote painting, server')

    c = tkinter.Canvas(master=master, width=canvas_width, height=canvas_height, bg='white')
    c.pack(expand=tkinter.NO)

    threading.Thread(target=recieve).start()
    master.after(100, after_callback)

    master.mainloop()