import copy
import VertexModel
from matplotlib import pyplot as plt
import Keating
import time

# Naive Implementation, how I would do it by hand
def Algorithm(vertex):
    SwapPaths = []
    for path in vertex.paths:
        alg_path = path_algorithm(vertex, path)
        if alg_path is not None:
            SwapPaths.append(alg_path)
    return SwapPaths

def path_algorithm(vertex, start_path):
    currPath = start_path
    if currPath.color == "blue":
        currSquare = currPath.squares[0]
        for red_path in vertex.RedPaths:
            if red_path.squares[0] == currSquare:
                return
    else:
        currSquare = currPath.squares[-1]
        for blue_path in vertex.BluePaths:
            if blue_path.squares[-1] == currSquare:
                return
    SwapPath = []
    SwapPath.append(currSquare)
    while(True):
        currEnterExit = currPath.EnterExit[currSquare]
        # Exit Condition
        for paths in vertex.paths:
            if paths == currPath or paths.color == currPath.color:
                continue
            for square in paths.squares:
                if square[0] == currSquare[0] and square[1] == currSquare[1]:
                    enter, exit = (currEnterExit[1], paths.EnterExit[square][1]) if currPath.color == "red" else (currEnterExit[0], paths.EnterExit[square][0])
                    if enter != exit:
                        currPath = paths
        if currPath.color == "red":
            currSquare = currPath.next_square(currSquare, reverse = True)
            if currSquare == -1:
                alg_path = VertexModel.Path(squares = SwapPath, color = "black")
                return alg_path
        else:
            currSquare = currPath.next_square(currSquare)
            if currSquare == -1:
                alg_path = VertexModel.Path(squares = SwapPath, color = "black")
                return alg_path
        SwapPath.append(currSquare)
        if currPath.color == "blue":
            if currSquare[1] == vertex.size[1]-1 and currEnterExit[1] == 1:
                break
        else:
            if currSquare[1] == 0 and currEnterExit[0] == 1:
                break
    alg_path = VertexModel.Path(squares = SwapPath, color = "black")
    return alg_path

def Graph(vertex, indiv = False):
    if indiv:
        for path in vertex.paths:
            pathing = path.pathing
            color = "black"  # Default color
            for i in range(len(pathing) - 1):
                color = direction(pathing[i], pathing[i+1])
                x = [point[0] for point in pathing[i:i+2]]
                y = [point[1] for point in pathing[i:i+2]]
                plt.plot(x, y, color=color)
            sizeX = vertex.size[0]
            sizeY = vertex.size[1]
            plt.xlim(0, sizeX)
            plt.ylim(0, sizeY)
            plt.xticks(range(0, sizeX + 1, 1))  # x-axis ticks from 0 to 10 with step 1
            plt.yticks(range(0, sizeY + 1, 1))  # y-axis ticks from 0 to 10 with step 1
            plt.grid(linestyle='-', linewidth=2)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()
    else:
        for path in vertex.paths:
            pathing = path.pathing
            color = "black"  # Default color
            for i in range(len(pathing) - 1):
                color = direction(pathing[i], pathing[i+1])
                x = [point[0] for point in pathing[i:i+2]]
                y = [point[1] for point in pathing[i:i+2]]
                plt.plot(x, y, color=color)
        sizeX = vertex.size[0]
        sizeY = vertex.size[1]
        plt.xlim(0, sizeX)
        plt.ylim(0, sizeY)
        plt.xticks(range(0, sizeX + 1, 1))  # x-axis ticks from 0 to 10 with step 1
        plt.yticks(range(0, sizeY + 1, 1))  # y-axis ticks from 0 to 10 with step 1
        plt.grid(linestyle='-', linewidth=2)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

# My attempt at sorting the paths based on their starting and ending squares
def sort_paths(vertexs):
    vertex_dictionary = {}
    for vertex in vertexs:
        boundaries = []
        for path in vertex.paths:
            start_square = path.squares[0]
            end_square = path.squares[-1]
            # In case order doesn't matter, you can just turn these into sets
            boundaries.append((start_square[0], start_square[1], end_square[0], end_square[1]))
        vertex_dictionary[vertex] = set(boundaries)
    sorted_groups = []
    for vertex in vertex_dictionary:
        group = [vertex2]
        boundaries = copy.copy(vertex_dictionary[boundaries])
        del vertex_dictionary[vertex]
        for vertex2 in vertex_dictionary:
            if boundaries.intersect(vertex_dictionary[vertex2]):
                group.append(vertex2)
                del vertex_dictionary[vertex2]
        sorted_groups.append(group)
    return sorted_groups


def direction(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    if dx > 0 or dy > 0:
        return "blue"  # Moving right or up
    elif dx < 0 or dy < 0:
        return "red"   # Moving left or down
    else:
        return "black"  # No movement

# Example case from the paper
b1 = VertexModel.Path([(0,0),(0,1), (0,2), (1,2), (2,2), (2,3), (2,4), (3,4), (4,4), (4,5), (5,5), (6,5), (6,6)], "blue")
r1 = VertexModel.Path([(0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (2,5), (2,6)],"red")
b2 = VertexModel.Path([(1,0), (1,1), (2,1), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (6,4), (7,4), (8,4), (8,5), (8,6)], "blue")
r2 = VertexModel.Path([(1,0), (1,1), (1,2), (1,3), (2,3), (3,3), (3,4), (3,5), (4,5), (4,6)], "red")
b3 = VertexModel.Path([(2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (10,1), (10,2), (10,3), (10,4), (10,5), (10,6)],"blue")
r3 = VertexModel.Path([(4,0), (4,1), (4,2), (4,3), (4,4), (5,4), (5,5), (5,6), (6,6)], "red")
v1 = VertexModel.Vertex([b1, r1, b2, r2, b3, r3])

# Uncommenting this gives you the first path detailed in the paper
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.RedPaths[0])])
# VertexModel.Graph(v2)
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.RedPaths[1])])
# VertexModel.Graph(v2)
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.RedPaths[2])])
# VertexModel.Graph(v2)
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.BluePaths[0])])
# VertexModel.Graph(v2)
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.BluePaths[1])])
# VertexModel.Graph(v2)
# v2 = VertexModel.Vertex([path_algorithm(v1, v1.BluePaths[2])])
# print(path_algorithm(v1, v1.BluePaths[2]).pathing)
# VertexModel.Graph(v2)
# This gives all path ouputs according to the algorithm for the vertex model described
s = time.perf_counter()
v2 = VertexModel.Vertex(Algorithm(v1))
print(time.perf_counter()-s)
Graph(v2, indiv = False)

# for partition in Keating.Partition([[2,2],[2]],[[2,1],[0]]).TabList(2):
#     print(partition[0], partition[1])
#     print(VertexModel.KeatingToJiang(partition, 2))
#     VertexModel.Graph(VertexModel.KeatingToJiang(partition, 2))
l = []
l = Algorithm(l)
# Assume this gives us all vertex model objects after running the swap algorithm on them all.