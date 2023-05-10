#!/usr/bin/env python3
import socket
import tkinter

address_to_server = ('localhost', 8888)
canvas_width = 450
canvas_height = 450


def paint(event):
    color = 'red'
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = x1 + 2, y1 + 2
    c.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    pack = (event.x.to_bytes(2, 'big') + event.y.to_bytes(2, 'big'))
    client.send(pack)


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    print("Client ready.")

    master = tkinter.Tk()
    master.title('Remote painting, client')

    c = tkinter.Canvas(master=master, width=canvas_width, height=canvas_height, bg='white')
    c.pack(expand=tkinter.NO)
    c.bind('<B1-Motion>', paint)

    master.mainloop()
