# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 2017

@author: Andrew
"""

def tuple_split(f):
    return [int(coord) for coord in f.readline().split(',')]

def world(filename):
    '''
    Parses world from argument file. File is 0-indexed.
    File should be in the following format:

    World dimensions
    Start
    Goal

    List of obstacles (separated by newlines)


    All values are tuple coordinates separated by commas.
    '''

    # World dimensions.
    f = open(filename)
    n, m = tuple_split(f)
    world = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Start and goal.
    start = tuple_split(f)
    goal = tuple_split(f)

    while True:
        if f.readline() == '':
            break

        # Obstacle, defined by two corners.
        corner1 = tuple_split(f)
        corner2 = tuple_split(f)

        for x in range(corner1[0], corner2[0] + 1):
            for y in range(corner1[1], corner2[1] + 1):
                world[y][x] = 1

    return world, start, goal
