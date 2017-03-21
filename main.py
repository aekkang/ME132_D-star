# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 2017

@author: Sith, Andrew
"""

import sys
from dstar import D_Star
from environment import world

def main(filename, size):
    actual_map, start, goal = world(filename)
    world_size = (len(actual_map[0]), len(actual_map))

    d_star = D_Star(world_size, start, goal)
    path = d_star.run(actual_map, size)

# To run, call on the command line:
#   > python main.py world<n> [cell_size]
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python main.py world<n> [cell_size]"
        exit(1)

    filename = sys.argv[1] + ".txt"

    if len(sys.argv) > 2:
        size = sys.argv[2]
    else:
        size = "small"

    main(filename, size)
