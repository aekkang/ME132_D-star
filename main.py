# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 2017

@author: Sith, Andrew
"""

def main(world):
    actual_map, start, goal = world
    world_size = (len(world[0]), len(world))

    d_star = D_star(aorld_size, start, goal)
    d_star.init_path()


environment = [[0 for i in range(21)] for j in range(31)]
start = (0, 0)
end = (20, 30)

for j in range(31):
    environment[j][10] = 1

world = (environment, start, goal)
main(world)
