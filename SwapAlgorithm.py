import VertexModel

# Naive Implementation, how I would do it by hand
def Algorithm(vertex):
    SwapPaths = []
    for path in vertex.paths:
        SwapPaths.append(path_algorithm(vertex, path))
    return SwapPaths

def path_algorithm(vertex, start_path):
    currPath = start_path
    currSquare = currPath.squares[0] if currPath.color == "blue" else currPath.squares[-1]
    currEnterExit = currPath.EnterExit[currSquare]
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
                # SwapPath.append(-1, -1)
                return VertexModel.Path(squares = SwapPath, color = "black")
        else:
            currSquare = currPath.next_square(currSquare)
            if currSquare == -1:
                return VertexModel.Path(squares = SwapPath, color = "black")
        SwapPath.append(currSquare)
        if currPath.color == "blue":
            if currSquare[1] == vertex.size[1]-1 and currEnterExit[1] == 1:
                break
        else:
            if currSquare[1] == 0 and currEnterExit[0] == 1:
                break
    return VertexModel.Path(squares = SwapPath, color = "black")


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

# This gives all path ouputs according to the algorithm for the vertex model described
v2 = VertexModel.Vertex(Algorithm(v1))
VertexModel.Graph(v2)