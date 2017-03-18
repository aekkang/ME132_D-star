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
    def __init__(self, world_size, start, goal):
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

    def cost(self, curr1, curr2):
        x1, y1 = curr1.loc
        x2, y2 = curr2.loc
        return self.c[y2][x2][y1][x1]

    def get(self, n):
        return self.world[n[1]][n[0]]

    def put(self, n, cell):
        self.world[n[1]][n[0]] = cell

    def open_get(self):
        item = self.Pqueue.get()
        curr = self.get(item[1])

        return (item[0], curr)

    def open_put(self, cell):
        cell.t = 'o'
        self.Pqueue.put( (cell.h, cell.loc) )

    def get_kmin(self):
        try:
            return sorted(self.Pqueue.queue)[0][0]
        except:
            return None

    def get_path(self, n):
        curr = n
        path = [curr]

        while True:
            cell = self.get(curr).b
            
            if cell == None:
                return None
            else:
                curr = cell.loc
                path.append(curr)

                if curr == self.goal:
                    import numpy as np
                    from copy import deepcopy
                    print
                    print "World:"
                    print "=================================================="
                    lol = deepcopy(self.world)
                    for i in range(len(lol)):
                        for j in range(len(lol[0])):
                            n = lol[i][j].loc
                            if n in path:
                                lol[i][j] = 1
                            else:
                                lol[i][j] = 0
                    print np.array(lol)
                    print

                    return path

    def get_neighbors(self, curr):
        neighbors = []
        loc = curr.loc
        x = loc[0]
        y = loc[1]

        min_y = max(0, y - 1)
        max_y = min(self.size[1] - 1, y + 1)
        min_x = max(0, x - 1)
        max_x = min(self.size[0] - 1, x + 1)                
        
        for j in xrange(min_y, max_y + 1):
            for i in xrange(min_x, max_x + 1):
                neighbors.append(self.get((i, j)))

        return neighbors

    ##################################################

    def init_path(self):
        goal = Cell(0, 0, 'g', 'o', self.goal)
        self.put(self.goal, goal)
        self.open_put(goal)

        while True:
            # import numpy as np
            # from copy import deepcopy
            # print
            # print "World:"
            # print "=================================================="
            # lol = deepcopy(self.world)
            # for i in range(len(lol)):
            #     for j in range(len(lol[0])):
            #         tag = lol[i][j].t
            #         if tag == 'c':
            #             lol[i][j] = 0
            #         elif tag == 'n':
            #             lol[i][j] = -1
            #         else:
            #             lol[i][j] = 0
            # print np.array(lol)
            # print

            k_min = self.process_state()

            if self.get(self.start).t == 'c':
                return self.get_path(self.start)
            elif k_min == None:
                return None

    def change_map(self, actual_map, curr):
        for sensed in self.get_neighbors(curr):
            for neighbor in self.get_neighbors(sensed):
                i, j = neighbor.loc

                if (actual_map[j][i]):
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
        x1, y1 = n1.loc
        x2, y2 = n2.loc

        self.c[y2][x2][y1][x1] = new_c
        
        if n1.t == 'c':
            curr = self.get(n1)
            self.insert(curr, curr.h)

        return self.get_kmin()

    def insert(self, curr, h_new):
        if curr.t == 'n':
            curr.k = h_new
        elif curr.t == 'o':
            curr.k = min(curr.k, h_new)
        elif curr.t == 'c':
            curr.k = min(curr.h, h_new)

        curr.h = h_new
        self.open_put(curr)

    def process_state(self):
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

        curr.t = 'c'

        return self.get_kmin()

    def run(self, actual_map):
        final_path = []

        path = self.init_path()
        if path == None:
            return None

        curr = self.start
        while curr != self.goal:
            self.change_map(actual_map, self.get(curr))
            if self.get(curr).t != 'c':
                path = self.navigate_map(curr)
            else:
                path = self.get_path(curr)

            if path == None:
                return None

            curr = path[1]
            print path
            final_path.append(curr)

        return final_path
