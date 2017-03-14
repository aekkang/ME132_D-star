from Tkinter import *

def cell(node, cell_size, type="new"):
    x, y = node

    x1 = cell_size * x
    y1 = cell_size * y
    x2 = cell_size * (x + 1) - 1
    y2 = cell_size * (y + 1) - 1

    if type == "new":
        canvas.create_rectangle(x1, y1, x2, y2)
    elif type == "obstacle":
        canvas.create_rectangle(x1, y1, x2, y2, fill="black")

def tuple_split(f):
    return [int(coord) for coord in f.readline().split(',')]

def world(filename, width, height):
    f = open(filename)
    n, m = tuple_split(f)
    cell_size = min(width / n, height / m)

    for x in range(n):
        for y in range(m):
            cell((x, y), cell_size)

    while True:
        if f.readline() == '':
            break

        corner1 = tuple_split(f)
        corner2 = tuple_split(f)

        for x in range(corner1[0], corner2[0]):
            for y in range(corner1[1], corner2[1]):
                cell((x, y), cell_size, type="obstacle")


if __name__ == "__main__":
    width, height = 800, 600

    root = Tk()
    root.geometry(str(width) + 'x' + str(height))
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()

    world("world1.txt", width, height)

    root.mainloop()

