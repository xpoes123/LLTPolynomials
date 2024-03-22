"""
This file contains both a path and vertex object that allow us to encode our vertex model
"""

import numpy as np
import copy
from decimal import Decimal
from itertools import product
from timeit import default_timer as timer
from matplotlib import pyplot as plt
import math
import Keating
# import tikzplotlib

colors = ["blue", "red", "black"]
class Vertex:
    # Paths consists of ''Path'' objects that are in the vertex model.
    def __init__(self, paths = []):
        self.paths = paths
        self.RedPaths = [i for i in paths if i.color == "red"]
        self.BluePaths = [i for i in paths if i.color == "blue"]
        maxX, maxY = 0,0
        for path in paths:
            for pathing in path.pathing:
                maxX = max(math.ceil(pathing[0]), maxX)
                maxY = max(math.ceil(pathing[1]), maxY)
        self.size = (maxX, maxY)

class Path:
    # Squares - list of squares that the path passes through
    # Pathing - Uses squares to calculate the half integral pathing it takes
    # Color - The intended color of the paht
    # EnterExit - Creates a dictionary that describes the way a path enters and exits a square
    def __init__(self, squares = [], color = "black") -> None:
        if color not in colors:
            raise Exception("Color Not Defined")
        self.squares = squares
        self.pathing = Path.fill(squares, color)
        self.color = color
        self.EnterExit = Path.enter_exit(self.squares)
    
    # Returns the next square in the path
    def next_square(self, square, reverse = False):
        if square in self.squares:
            if not reverse and self.squares.index(square) > len(self.squares):
                # We are on a blue path and we have reached the end
                return -1
            if reverse and self.squares.index(square) == 0:
                # We are on a red path and we have reached the end
                return -1
            return self.squares[self.squares.index(square) + 1] if not reverse else self.squares[self.squares.index(square) - 1]
        else:
            raise Exception("Square not found")
    # Updates pathing to be accurate given squares
    def fill(squares, color = "black"):
        if color == "black":
            if squares[0][1] != 0:
                vPath = []
                FirstSquare = squares[0]
                vPath.append((FirstSquare[0] + 0.5, FirstSquare[1] + 1))
                vPath.append((FirstSquare[0] + 0.5, FirstSquare[1] + 0.5))
                for i in squares[1:]:
                    vPath.append((i[0] + 0.5, i[1] + 0.5))
                LastSquare = squares[-1]
                print(LastSquare)
                if LastSquare[1] == 0:
                    vPath.append((LastSquare[0] + 0.5, 0))
                else:
                    vPath.append((LastSquare[0] + 0.5, LastSquare[1] + 1))
                return vPath
        vPath = []
        FirstSquare = squares[0]
        vPath.append((FirstSquare[0] + 0.5, 0))
        vPath.append((FirstSquare[0] + 0.5, FirstSquare[1] + 0.5))
        for i in squares[1:]:
            vPath.append((i[0] + 0.5, i[1] + 0.5))
        LastSquare = squares[-1]
        # print(LastSquare)
        if LastSquare[1] == 0:
            vPath.append((LastSquare[0] + 0.5, 0))
        else:
            vPath.append((LastSquare[0] + 0.5, LastSquare[1] + 1))
        return vPath

    # Creates a dictionary of tuples on the enter and exit of each square. Encodes coming from the top or bottom is 1, and left and right are -1
    def enter_exit(squares):
        EnterExit = {}
        enter, exit = 1, 0
        for index, square in enumerate(squares[:-1]):
            if square[0] < squares[index + 1][0]:
                exit = -1
            else:
                exit = 1
            EnterExit[square] = (enter, exit)
            enter = exit
        EnterExit[squares[-1]] = (enter, 1)
        return EnterExit

# Graphs a vertex object
def Graph(vertex):
    for path in vertex.paths:
        pathing = path.pathing
        match path.color:
            case "blue":
                pathing = [(i[0] - 0.1, i[1]) for i in path.pathing]
            case "red":
                pathing[1:-1] = [(i[0], i[1] + 0.1) for i in path.pathing[1:-1]]
        x = [i[0] for i in pathing]
        y = [i[1] for i in pathing]
        plt.plot(x, y, color = path.color)
    sizeX = vertex.size[0]
    sizeY = vertex.size[1]
    plt.xlim(0, sizeX)
    plt.ylim(0, sizeY)
    plt.xticks(range(0, sizeX + 1, 1))  # x-axis ticks from 0 to 10 with step 1
    plt.yticks(range(0, sizeY + 1, 1))  # y-axis ticks from 0 to 10 with step 1
    plt.grid(linestyle='-', linewidth=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def KeatingToJiang(keatingPaths, nVars):
    jiangPaths = []
    pathOffset = 0
    for path in keatingPaths:
        nextJiangPath = []
        x = -1 + pathOffset
        y = -1
        pathOffset += -1
        firstNonZero = False
        for xVal in path:
            x += 1
            if (not firstNonZero) and xVal > 0:
                firstNonZero = True
            if y >= 0 and firstNonZero:
                nextJiangPath.append((x,y))
            if xVal > nVars:
                while y < nVars-1:
                    y += 1
                    nextJiangPath.append((x,y))
            elif xVal > y+1:
                while y+1 < xVal:
                    y += 1
                    nextJiangPath.append((x,y))     
        jiangPaths.append(Path(nextJiangPath, "red"))
    return Vertex(jiangPaths)
