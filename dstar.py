# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:04:31 2017

@author: Sith, Andrew
"""

import math
import Queue

class Cell:

    # Access cell values:
    #   h:      path cost
    #   k:      smallest value of h seen so far
    #   b:      back pointer
    #   t:      tag ('c' - closed; 'o' - open; 'n' - new)
    def __init__(self, h, k, b, t):
        self.h = h
        self.k = k
        self.b = b
        self.t = t


class D_Star:
    
    # Init function with robot world's decomposition
    # Start (x,y) and Goal (x,y) 
    def __init__(self, world_size, start, goal):
        World_X = world_size[0]
        World_Y = world_size[1]
        
        self.start = start
        self.goal = goal
        self.size = world_size
        self.world = [[Cell(None, None, None, 'n') for _ in range(World_X)] for _ in range(World_Y)]
        self.Pqueue = Queue.PriorityQueue() # Open list
        self.c = [[[[None for _ in range(World_X)] for _ in range(World_Y)]
                 for _ in range(World_X)] for _ in range(World_Y)] # Edge costs.

    def cost(self, n1, n2):
        return c[n2[1]][n2[0]][n1[1]][n1[0]]
                       
    def init_path(self):
        curr = self.goal
        self.world[self.goal[1]][self.goal[0]] = Cell(0, 0, 'g', 'o')
        
        while (curr != self.start):
            try:
                self.init_neighbors(curr)
                curr = self.Pqueue.get()
            except:
                # No path found
                return False

        return True

    def get_neighbors(self, curr):
        neighbors = []

        y = curr[0]
        x = curr[1]

        min_y = max(0, y - 1)
        max_y = min(self.size[1] - 1, y + 1)
        min_x = max(0, x - 1)
        max_x = min(self.size[0] - 1, x + 1)                
        
        for j in xrange(min_y, max_y):
            for i in xrange(min_x, max_x):
                neighbors.append((i, j))

        return neighbors

    def init_neighbors(self, curr):
        # Limit to world border
        neighbors = self.get_neighbors(curr)

        for (i, j) in neighbors:
            if (i,j) == curr:
                pass
            else:
                k = self.world[curr[1]][curr[0]][1]
                dist = math.hypot(i - curr[0], j - curr[1]) + k
                if (world[j][i].k == None or world[j][i].k > dist): 
                    self.world[j][i] = Cell(dist, dist, curr, 'o')
                    self.Pqueue.put( (dist, (i,j)) )

        self.world[curr[1]][curr[0]].t = 'c'

        return 0

    # Try to navigate through obstacles with actual world map
    def navigate_map(self, actual_map):
        curr = self.start
        
        while (curr ! = self.goal):
            x = curr[0]
            y = curr[1]
            
            sensed = self.get_neighbors(curr)

            for n_sensed in sensed:
                i, j = n_sensed
                neighbors = self.get_neighbors((i, j))

                if (actual_map[j][i]):
                    for n_neighbor in neighbors:
                        modify_costs(n_sensed, n_neighbor, float("inf"))
                
    def change_map(self, curr):
        curr = self.goal
        self.world[self.goal[1]][self.goal[0]] = Cell(0, 0, 'g', 'o')
        
        while (curr != self.start):
            try:
                self.init_neighbors(curr)
                curr = self.Pqueue.get()
            except:
                # No path found
                return False

        return True
                
    def modify_costs(self, n1, n2, new_c):
        c[n2[1]][n2[0]][n1[1]][n1[0]] = new_c
        
        if n1.t == 'c':
            self.Pqueue.put( (self.world[j][i].k , (i,j)) )
            self.world[j][i].t = 'o'

        return sorted(self.Pqueue.queue)[0][0]
