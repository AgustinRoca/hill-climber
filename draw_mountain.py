# create a 2d map of the world
import random
import time
import math
from communication.client.client import MountainClient

class World:
    def __init__(self, draw_radius, radius):
        self.draw_radius = draw_radius
        self.radius = radius
        self.ratio = radius/draw_radius
        self.map = [[{"mark": -1, "summit": False} for x in range(self.draw_radius*2+1)] for y in range(self.draw_radius*2+1)]
        self.teams = []
        self.client = MountainClient('10.42.0.1', 8888)
        self.green = "\x1b[32;20m"
        self.reset = "\x1b[0m"

    def print_map(self):
        for (i, row) in enumerate(self.map):
            for col in row:
                if col['mark'] == -1:
                    c = '. '
                elif col['mark'] == 0:
                    c = '  '
                elif col['mark'] > 0:
                    c = chr(col['mark']+64) + ' ' # f"{col:2d}"
                    if col['summit']:
                        c = self.green + c + self.reset
                print(c, end='')
            if (i==1):
                print(" Teams:", end='')
            elif (1<i<len(self.teams)+2):
                print(f" {chr(i+63)}. {self.teams[i-2]}", end='')
            print()

    def create_map(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if (col - self.draw_radius)**2 + (row - self.draw_radius)**2 <= self.draw_radius**2:
                    self.map[row][col]['mark'] = -1
                else:
                    self.map[row][col]['mark'] = 0

    def put_mark(self, pos):
        row = int((self.radius-pos[1])/self.ratio)
        col = int((self.radius+pos[0])/self.ratio)
        summit = pos[2]
        team = pos[3]
        if team not in self.teams:
            self.teams.append(team)
        if not self.map[row][col]['summit']:
            self.map[row][col]['mark'] = self.teams.index(team)+1
            self.map[row][col]['summit'] = summit




while True:


    w = World(23, 23000)
    w.create_map()
    pos_list = []     #TODO: get positions from server
    try:
        data = w.client.get_data()
    except:
        pass

    for team in data:
        for hiker in data[team]:
            pos_list.append((data[team][hiker]['x'],data[team][hiker]['y'], data[team][hiker]['cima'], team))

    # Alternative:

    for pos in pos_list:
        w.put_mark(pos)

    w.print_map()
    time.sleep(1)




