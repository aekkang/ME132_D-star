# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 2017

@author: Andrew
"""

from Tkinter import *
from environment import world
from time import sleep

class Graphics:

    def __init__(self, world):
        cell_size = 15
        width = len(world[0])
        height = len(world)
        c_width = width * cell_size
        c_height = height * cell_size

        self.root = Tk()
        self.root.geometry(str(c_width) + 'x' + str(c_height))
        self.canvas = Canvas(self.root, width=c_width, height=c_height)
        self.canvas.pack()
        # done = False

        self.cells = [[0 for _ in range(width)] for _ in range(height)]

        for j in range(height):
            for i in range(width):
                if world[j][i]:
                    self.cells[j][i] = self.cell((j, i), cell_size, type="obstacle")
                else:
                    self.cells[j][i] = self.cell((j, i), cell_size, type="new")

        self.root.update()
        sleep(1)

    def cell(self, node, cell_size, type="new"):
        x, y = node

        x1 = cell_size * x
        y1 = cell_size * y
        x2 = cell_size * (x + 1) - 1
        y2 = cell_size * (y + 1) - 1

        if type == "new":
            return self.canvas.create_rectangle(x1, y1, x2, y2)
        elif type == "obstacle":
            return self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def display(self, path, obstacles, done=False):
        for (i, j) in path:
            self.canvas.itemconfig(self.cells[j][i], fill="red")
        for (i, j) in obstacles:
            self.canvas.itemconfig(self.cells[j][i], fill="black")

        if done:
            self.root.mainloop()
        else:
            self.root.update()

# def tuple_split(f):
#     return [int(coord) for coord in f.readline().split(',')]

# def world(filename, width, height):
#     f = open(filename)
#     n, m = tuple_split(f)
#     cell_size = min(width / n, height / m)

#     for x in range(n):
#         for y in range(m):
#             cell((x, y), cell_size)

#     while True:
#         if f.readline() == '':
#             break

#         corner1 = tuple_split(f)
#         corner2 = tuple_split(f)

#         for x in range(corner1[0], corner2[0]):
#             for y in range(corner1[1], corner2[1]):
#                 cell((x, y), cell_size, type="obstacle")

# def display():
#     pass


if __name__ == "__main__":
    width, height = 800, 600

    root = Tk()
    root.geometry(str(width) + 'x' + str(height))
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    done = False

    world("world1.txt", width, height)

    while not done:
        for ball in bouncing_balls:
            ball.step()
        root.update()

