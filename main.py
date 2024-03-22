import VertexModel
import Keating
import SwapAlgorithm

def main(redBoundary, blueBoundary, nVars):
    for redPartition in Keating.Partition(redBoundary[0],redBoundary[1]).TabList(nVars):
        redJiangPartition = VertexModel.KeatingToJiang(redPartition, nVars, "red")
        for bluePartition in Keating.Partition(blueBoundary[0],blueBoundary[1]).TabList(nVars):
            blueJiangPartition = VertexModel.KeatingToJiang(bluePartition, nVars, "blue")
            fullVertexModel = VertexModel.Vertex(redJiangPartition.paths+blueJiangPartition.paths)
            VertexModel.Graph(fullVertexModel)
            VertexModel.Graph(VertexModel.Vertex(SwapAlgorithm.Algorithm(fullVertexModel)))

def example():
    redTop = [[3],[2]]
    redBottom = [[2],[0]]
    blueTop = [[3],[2]]
    blueBottom = [[1],[0]]
    n = 2
    main([redTop, redBottom], [blueTop, blueBottom], n)

example()