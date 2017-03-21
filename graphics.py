# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 2017

@author: Andrew
"""

from Tkinter import *
from environment import world
from time import sleep

class Graphics:

    def __init__(self, world, size="small"):
        if size == "large":
            cell_size = 50
        else:
            cell_size = 15

        width = len(world)
        height = len(world[0])
        c_height = int(height * cell_size)
        c_width = int(width * cell_size)

        self.root = Tk()
        # TODO: This is confusing...
        self.root.geometry(str(c_height) + 'x' + str(c_width))
        self.canvas = Canvas(self.root, width=c_height, height=c_width)
        self.canvas.pack()

        self.cells = [[0 for _ in range(width)] for _ in range(height)]

        for i in range(height):
            for j in range(width):
                self.cells[i][j] = self.cell((i, j), cell_size)

        self.root.update()
        sleep(1)

    def cell(self, node, cell_size):
        x, y = node

        x1 = cell_size * x
        y1 = cell_size * y
        x2 = cell_size * (x + 1) - 1
        y2 = cell_size * (y + 1) - 1

        return self.canvas.create_rectangle(x1, y1, x2, y2)

    def display(self, path, obstacles, done=False):
        for (i, j) in path:
            self.canvas.itemconfig(self.cells[i][j], fill="red")
        for (i, j) in obstacles:
            self.canvas.itemconfig(self.cells[i][j], fill="black")

        if done:
            self.root.mainloop()
        else:
            self.root.update()
        sleep(0.2)
