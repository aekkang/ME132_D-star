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
    def __init__(self, h, k, b, t, loc):
        self.h = h
        self.k = k
        self.b = b
        self.t = t
        self.loc = loc


class D_Star:
    
    # Init function with robot world's decomposition
    # Start (x,y) and Goal (x,y) 
    def __init__(self, world, world_size, start, goal):
        World_X = world_size[0]
        World_Y = world_size[1]
        
        self.start = start
        self.goal = goal
        self.size = world_size
        self.world = [[Cell(None, None, None, 'n', (i, j)) for i in range(World_X)] for j in range(World_Y)]
        self.Pqueue = Queue.PriorityQueue() # Open list
        self.c = [[[[None for _ in range(World_X)] for _ in range(World_Y)]
                 for _ in range(World_X)] for _ in range(World_Y)] # Edge costs.

        for j1 in range(World_Y):
            for i1 in range(World_X):
                for j2 in range(World_Y):
                    for i2 in range(World_X):
                        self.c[j1][i1][j2][i2] = math.hypot(i2 - i1, j2 - j1)

    def cost(self, n1, n2):
        return c[n2[1]][n2[0]][n1[1]][n1[0]]

    def get(self, n):
        return self.world[n[1]][n[0]]

    def put(self, n, cell):
        self.world[n[1]][n[0]] = cell
        self.Pqueue.put( (cell.h, cell) )

    def open_get(self):
        curr = self.Pqueue.get()

        return (curr[0], self.get(curr[1]))

    def get_kmin(self):
        try:
            return sorted(self.Pqueue.queue)[0][0]
        except:
            return None

    def get_path(self, n):
        curr = n
        path = [curr]

        while True:
            curr = self.get(curr).b
            path.append(curr)

            if curr == self.goal:
                return path
            elif curr == None:
                return None

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
                neighbors.append(self.get(i, j))

        return neighbors

    ##################################################

    def init_path(self):
        self.put(self.goal, Cell(0, 0, 'g', 'o', self.goal))

        while True:
            k_min = self.process_state()

            if k_min == None:
                return None
            elif self.get(self.start) == 'c':
                return self.get_path(self.start)

    def change_map(self, actual_map, curr):
        x = curr[0]
        y = curr[1]

        for sensed in self.get_neighbors(curr):
            neighbors = self.get_neighbors(sensed)
            i, j = neighbor

            if (actual_map[j][i]):
                for neighbor in neighbors:
                    self.modify_costs(sensed, neighbor, float("inf"))

    # Try to navigate through obstacles with actual world map
    def navigate_map(self, curr):
        while True:
            k_min = self.process_state()
            
            if k_min == None:
                return None
            elif self.get(curr).h <= k_min:
                return self.get_path(curr)

    def modify_costs(self, n1, n2, new_c):
        c[n2[1]][n2[0]][n1[1]][n1[0]] = new_c
        
        if n1.t == 'c':
            curr = self.get(n1)
            self.insert(n1, curr.h)

        return self.get_kmin()

    def insert(n, h_new):
        if n.t == 'n':
            n.k = h_new
        elif n.t == 'o':
            n.k = min(k, h_new)
        elif n.t == 'c':
            n.k = min(n.h, h_new)

        n.h = h_new
        n.t = 'o'
        self.Pqueue.put( (n.h, n.loc) )

    def process_state():
        try:
            k_old, curr = self.open_get()
        except:
            return None

        if k_old < curr.h:
            for neighbor in self.get_neighbors(curr):
                if curr.t != 'n' and curr.h <= k_old \
                and curr.h > neighbor.h + self.cost(neighbor, curr):
                    curr.b = neighbor
                    curr.h = neighbor.h + self.cost(neighbor, curr)
        elif k_old == curr.h:
            for neighbor in self.get_neighbors(curr):
                if (neighbor.t == 'n') \
                or (neighbor.b == curr and neighbor.h != curr.h + self.cost(curr, neighbor)) \
                or (neighbor.b != curr and neighbor.h > curr.h + self.cost(curr, neighbor)):
                    neighbor.b = curr
                    self.insert(neighbor, curr.h + self.cost(curr, neighbor))
        else:
            for neighbor in self.get_neighbors(curr):
                if neighbor.t == 'n' \
                or (neighbor.b == curr and neighbor.h != curr.h + self.cost(curr, neighbor)):
                    neighbor.b = curr
                    self.insert(neighbor, curr.h + self.cost(curr, neighbor))
                elif neighbor.b != curr and neighbor.h > curr.h + self.cost(curr, neighbor):
                    self.insert(curr, curr.h)
                elif neighbor.b != curr and curr.h > neighbor.h + self.cost(curr, neighbor) \
                and neighbor.t == 'c' and neighbor.h > k_old:
                    self.insert(neighbor, neighbor.h)

        return self.get_kmin()

    def run(self, actual_map):
        final_path = []

        path = self.init_path()
        if path == None:
            return None

        curr = self.start
        while curr != self.goal:
            self.change_map(actual_map, curr)
            path = self.navigate_map(curr)

            if path == None:
                return None

            curr = path[1]
            final_path.append(curr)

        return final_path
