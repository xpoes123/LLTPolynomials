import VertexModel
import Keating
import SwapAlgorithm

def main(redBoundary, blueBoundary, nVars):
    n=0
    groupingDict = {}
    for redPartition in Keating.Partition(redBoundary[0],redBoundary[1]).TabList(nVars):
        redJiangPartition = VertexModel.KeatingToJiang(redPartition, nVars, "red")
        for bluePartition in Keating.Partition(blueBoundary[0],blueBoundary[1]).TabList(nVars):
            n += 1
            #print(str(n))
            blueJiangPartition = VertexModel.KeatingToJiang(bluePartition, nVars, "blue")
            fullVertexModel = VertexModel.Vertex(redJiangPartition.paths+blueJiangPartition.paths)
            groupingLabel = []
            for path in SwapAlgorithm.Vertex_Algorithm(fullVertexModel):
                groupingLabel.append(SwapAlgorithm.get_start_end(VertexModel.Vertex([path])))
            groupingLabelStr = str(groupingLabel)
            if not(groupingLabelStr in groupingDict):
                groupingDict[groupingLabelStr] = []
                VertexModel.Graph(fullVertexModel)
                #SwapAlgorithm.Graph(VertexModel.Vertex(SwapAlgorithm.Vertex_Algorithm(fullVertexModel)))
            groupingDict[groupingLabelStr].append([redPartition, bluePartition])
            #VertexModel.Graph(fullVertexModel)
            #SwapAlgorithm.Graph(VertexModel.Vertex(SwapAlgorithm.Vertex_Algorithm(fullVertexModel)))
    outputStr = ""
    for groupingStr in groupingDict:
        allPathConfigs = groupingDict[groupingStr]
        outputStr += "Polynomial for grouping " + groupingStr + ": " + Keating.LLT.GroupedPoly(nVars,allPathConfigs) + "\n"
    return outputStr

def example():
    redTop = [[2],[0]]
    redBottom = [[0],[0]]
    blueTop = [[3],[2]]
    blueBottom = [[0],[0]]
    n = 3
    print(main([redTop, redBottom], [blueTop, blueBottom], n))

example()