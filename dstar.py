# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:04:31 2017

@author: Sith
"""

import numpy as np
import math
import Queue

class D_Star:
    
    # Init function with robot world's decomposition
    # Each cell has [h,k,b] - Same variable as the link
    # Start (x,y) and Goal (x,y) 
    def __init__(self, world_size, start, goal):
        World_X = world_size[0]
        World_Y = world_size[1]
        
        self.start = start
        self.goal = goal
        self.size = world_size
        self.world = np.array([[[-1,-1,-1] for i in range(World_X)] for j in range(World_Y)])
        # Priority Queue sorts by first element I think.
        self.Pqueue = Queue.PriorityQueue()
                       
    def init_path(self):
        current = self.goal
        self.world[self.goal[1]][self.goal[0]] = [0,0,"goal"]
        
        while (current != self.start):
            self.init_neighbors(current)
            current = self.Pqueue.get()
        return 0
        
    def init_neighbors(self, current):
        # Limit to world border
        min_y = max(0, current[1] - 1)
        max_y = min(self.size[1] - 1, current[1] + 1)

        min_x = max(0, current[0] - 1)
        max_x = min(self.size[0] - 1, current[0] + 1)
        
        for j in xrange(min_y, max_y):
            for i in xrange(min_x, max_x):
                if (i,j) == current:
                    pass
                else:
                    k = self.world[current[1]][current[0]][1]
                    distance = math.hypot(i - current[0], j - current[1]) + k
                    if (world[j][i][1] == -1 or world[j][i] > distance): 
                        self.world[j][i] = [distance, distance, current]
                        self.Pqueue.put( (distance, [i,j]) )
        return 0
                    
    # Try to navigate through obstacles with actual world map
    def navigate(self, actual_map):
        path = []
        path.append(self.start)
        current = self.start
        
        while (current ! = self.goal):
            x = current[0]
            y = current[1]
            
            if (actual_map[y][x]):
                # Page 47 of slides
                # Update cost and push neightbors onto stack
                self.world[x][y][0] = 10000

                min_y = max(0, y - 1)
                max_y = min(self.size[1] - 1, y + 1)
                min_x = max(0, x - 1)
                max_x = min(self.size[0] - 1, x + 1)                
                
                for j in xrange(min_y, max_y):
                    for i in xrange(min_x, max_x):
                        if (i,j) != current:
                            self.Pqueue.put( (self.world[j][i][1] , [i,j]) )
                
        return path
        
        