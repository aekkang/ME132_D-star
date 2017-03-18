# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 2017

@author: Sith, Andrew
"""

from dstar import D_Star

def main(world):
    actual_map, start, goal = world
    world_size = (len(actual_map[0]), len(actual_map))

    d_star = D_Star(world_size, start, goal)
    path = d_star.run(actual_map)
    print path


environment = [[0 for i in range(21)] for j in range(31)]
start = (0, 0)
goal = (20, 30)




for j in range(31):
    if j == 15:
        continue
    environment[j][5] = 1

import numpy as np
print
print "World:"
print "=================================================="
print np.array(environment)
print


world = (environment, start, goal)
main(world)
