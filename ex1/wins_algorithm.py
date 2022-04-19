# coding=utf-8
import sys
import time
import copy
from ortools.graph import pywrapgraph
from ortools.sat.python import cp_model

class Edge:
    def __init__(self, i, j, ij, ji):
        self.i = i
        self.j = j
        self.ij = ij
        self.ji = ji
    
    def show(self):
        string = "(" + str(self.i) + "," + str(self.j) + ") - cost_{ij} = " + str(self.ij) + "; cost_{ji} = " + str(self.ji) + ";"
        return string

class Vertice:
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges

    def addEdge(self,edge):
        self.edges.append(edge)

    def getEdges(self):
        return self.edges

    def show(self):
        string = (self.name + "::Edges::")
        count = 0
        for edge in self.edges:
            if count > 0:
                string = string + ","
            if edge.i == self.name:
                string = string + " (" + str(edge.i) + "," + str(edge.j) + "," + str(edge.ij) + "," + str(edge.ji) + ")"
            else:
                string = string + " (" + str(edge.j) + "," + str(edge.i) + "," + str(edge.ji) + "," + str(edge.ij) + ")"
            count = count + 1
        return string

class ArcVertice:
    def __init__(self, name, outdeg, indeg, demand):
        self.name = name
        self.outdeg = outdeg
        self.indeg = indeg
        self.demand = demand

    def addArc(self,edge):
        self.edges.append(edge)

    def getArcs(self):
        return self.edges

    def incIndeg(self):
        self.indeg = self.indeg + 1

    def incOutdeg(self):
        self.outdeg = self.outdeg + 1
    
    def recalcDemand(self):
        self.demand = self.outdeg - self.indeg

    def show(self):
        string = (str(self.name) + "::Outdeg::" + str(self.outdeg) + "::Indeg::" + str(self.indeg) + "::Demand::" + str(self.demand))
        return string



def euler_tour(arcsPrimePrime, startNode):
    arcsStack = copy.copy(arcsPrimePrime)
    curNode = startNode
    tour = [curNode] 

    while(len(arcsStack) > 0):
        arc = None
        for i in range(len(arcsStack)):
            if(arcsStack[i][0] == curNode):
                arc = arcsStack.pop(i)
                break
               
        if (arc is None):
            print("CRITICAL FAILURE")
            exit(1)
 
        curNode = arc[1]
        tour.append(arc[1])

        if(curNode == startNode and len(arcsStack) > 0):
            curStack = []           
            curCurNode = -1
            for i in range(len(tour)-1, -1, -1):
                curArcIndex = -1
                for j in range(len(arcsStack)):
                    if(arcsStack[j][0] == tour[i]):
                        curArcIndex = j
                        break

                if (curArcIndex < 0):
                    curStack.append(tour.pop(i))
                else:
                    curCurNode = tour[i]
                    tour.pop(i)
                    break

            if (curCurNode < 0):
                print("CRITICAL FAILURE (2)")

                print("<<<<<<<<<<Start node: " + str(startNode) + ">>>>>>>>>>>>")
                print(arcsStack)
                print(tour)
                print(curStack)
                print(curCurNode)
                print("<<<<<<<<<<>>>>>>>>>>")
                exit(1)

            print("<<<<<<<<<<Start node: " + str(startNode) + ">>>>>>>>>>>>")
            print(tour)
            print(curStack)
            print(curCurNode)
            print("<<<<<<<<<<>>>>>>>>>>")
            return tour + euler_tour(arcsStack, curCurNode) + curStack

    return tour

def parse_input_file():
    def parse_input_line(line, edgeList):
        split_line = line.split('coste')

        split_part = split_line[0].split(',')
        from_num = int((split_part[0]).strip()[1:])
        to_num = int((split_part[1]).strip()[:-1])
        
        split_part_2 = split_line[1].strip().split(' ')
        from_to_cost = int(split_part_2[0])
        to_from_cost = int(split_part_2[len(split_part_2) - 1])

        edgeList.append(Edge(str(from_num), str(to_num), from_to_cost, to_from_cost))

    # Get the total number of args passed to the demo.py
    total = len(sys.argv)
     
    # Get the arguments list 
    cmdargs = str(sys.argv)

    if (total != 2):
        print("Error: synopsis is: program file")
        quit()

    input_file_path = sys.argv[1]
    input_file = open(input_file_path, "r")

    for i in range(2):
        print(input_file.readline())

    vertice_line = input_file.readline()
    vertices = int(vertice_line.split(':')[1])

    edgeList = []
    for x in input_file:
        if (x[0] == '('):
            parse_input_line(x, edgeList)

    input_file.close()
    
    # Create vertice set   
    vertices = []
    for edge in edgeList:
        foundI = False
        foundJ = False
        for vertice in vertices:
            if (vertice.name == edge.i):
                foundI = True
                vertice.addEdge(edge)
            if (vertice.name == edge.j):
                foundJ = True
                vertice.addEdge(edge)
        
        if (foundI == False):
            vertices.append(Vertice(edge.i, [edge]))
        if (foundJ == False):
            vertices.append(Vertice(edge.j, [edge]))

       
    
    return (vertices, edgeList)

def is_eulerian(graph):
    isEulerian = True
    for vertice in graph[0]:
        print(vertice.show())
   
    oddVertices = [] 
    for vertice in graph[0]:
        if (len(vertice.getEdges()) % 2 == 1):
            isEulerian = False
            oddVertices.append(vertice)
            print(vertice.show())
    
            

    return (isEulerian, oddVertices)

def to_eulerian_proc(graph, oddVertices):
    print("Graph is NOT eulerian! - Starting the conversion to eulerian proc")
   
    vertices = copy.deepcopy(graph[0])
    edges =  copy.deepcopy(graph[1])
    oddVertices = copy.deepcopy(oddVertices)

    #------------------------------------------------------------------------------------
    # 2.(a): Calculate ce = (cij + cji) / 2
    for vertice in vertices:
        for edge in vertice.edges:
            ce = (edge.ij + edge.ji) / 2
            edge.ij = ce
            edge.ji = ce

    for edge in edges:
        ce = (edge.ij + edge.ji) / 2
        edge.ij = ce
        edge.ji = ce

    for vertice in oddVertices:
        for edge in vertice.edges:
            ce = (edge.ij + edge.ji) / 2
            edge.ij = ce
            edge.ji = ce
    
    print("2.(a) complete")
    #------------------------------------------------------------------------------------
    # 2.(b): Find shortest paths between odd vertices (using or-tools dijkstra) 
    def costs(i,j):
        verticeI = vertices[i]
        verticesJ = vertices[j]

        for edge in verticeI.edges:
            if edge.j == verticesJ.name:
                return edge.ij
            if edge.i == verticesJ.name:
                return edge.ji
        
        return 999999
        
    oddVerticesIndexes = []
    count = 0
    for vertice in vertices:
        for verticeB in oddVertices:
            if vertice.name == verticeB.name:
                oddVerticesIndexes.append(count)
                break
        count = count + 1
   
    solutions = []

    print("2.(b) - first part complete, we have: " + str(len(oddVertices)) + " odd vertices")
    print("this gives us in total: " + str(len(oddVertices) * (len(oddVertices) - 1) / 2) + " comparisons")
    curCount = 0
    for startIndex in range(len(oddVertices)):

        startTime = time.time()

        for endIndex in range(startIndex+1,len(oddVerticesIndexes)):
            solution = pywrapgraph.DijkstraShortestPath(len(vertices), oddVerticesIndexes[startIndex], oddVerticesIndexes[endIndex], costs, 888888)
            solutionCost = 0
            for solutionIndex in range(1,len(solution[1])):
                curCost = costs(solution[1][solutionIndex-1], solution[1][solutionIndex])
                solutionCost = solutionCost + curCost
            solutions.append((oddVerticesIndexes[startIndex], oddVerticesIndexes[endIndex], solution[1], solutionCost ))
        curCount = curCount + 1

        endTime = time.time()
        print(endTime-startTime)
        print("Progress: " + str(curCount) + "/" + str(len(oddVertices)))

    # Print shortest paths:
    """
    for solution in solutions:
        print(solution)
    """

    print("2.(b) complete")
    #------------------------------------------------------------------------------------
    # 2.(c): Find minimum cost perfect matching (or-tools cp_model):

    model = cp_model.CpModel()
    x = []
    for solution in solutions:
        x.append((solution[0], solution[1], model.NewIntVar(0,1000, 'x' + str(solution[0]) + str(solution[1])), solution[3]))

    for oddIndex in oddVerticesIndexes:
        cs = 0
        for xij in x:
            if (xij[0] == oddIndex):
                cs = cs + xij[2]
            if (xij[1] == oddIndex):
                cs = cs + xij[2]
        model.Add(cs == 1)

    cs = 0
    for xij in x:
        cs = cs + (xij[3] * xij[2])
    model.Minimize(cs)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    print("2.(c) complete")
    #------------------------------------------------------------------------------------
    # 2.(d): Add to original path set

    orVertices = graph[0]
    orEdges = graph[1]

    """
    for xij in x:
        print(str(solver.Value(xij[2])))
    """
    
    index = 0
    for xij in x:
        if (solver.Value(xij[2]) == 1):
            # Use path  
            solution = solutions[index]
            path = solution[2]
            
            for vi in range(1, len(path)):
                verticeA = orVertices[path[vi - 1]]
                verticeB = orVertices[path[vi]]
                
                newEdge = None
                for edge in verticeA.edges:
                    if (edge.i == verticeA.name and edge.j == verticeB.name):
                        newEdge = copy.copy(edge)
                        break
                    if (edge.j == verticeA.name and edge.i == verticeB.name):
                        newEdge = copy.copy(edge)
                        break
                if newEdge is not None:
                    verticeA.edges.append(newEdge)
                    orEdges.append(newEdge) # Add only once
                else:
                    print("NEW EDGE IS NONE!(1)")

                for edge in verticeB.edges:
                    if (edge.i == verticeB.name and edge.j == verticeA.name):
                        newEdge = copy.copy(edge)
                        break
                    if (edge.j == verticeB.name and edge.i == verticeA.name):
                        newEdge = copy.copy(edge)
                        break
                if newEdge is not None:
                    verticeB.edges.append(newEdge)
                else:
                    print("NEW EDGE IS NONE!(2)")
        index = index + 1

    print("2.(d) - complete")
    print("Eulerian conversion complete")
    return (orVertices, orEdges)
    #------------------------------------------------------------------------------------ 
    
   
def wins_algorithm(graph):
    
    arcsVertices = []
    arcs = []
    for edge in graph[1]:
        if edge.ij <= edge.ji:
            arcs.append((int(edge.i),int(edge.j),edge.ij,999999, edge.ji))

            vertexFound = False
            for vertex in arcsVertices:
                if (vertex.name == int(edge.i)):
                    vertexFound = True
                    vertex.incOutdeg()

            if vertexFound == False:
                arcsVertices.append(ArcVertice(int(edge.i), 1, 0, 0))
            vertexFound = False
            for vertex in arcsVertices:
                if (vertex.name == int(edge.j)):
                    vertexFound = True
                    vertex.incIndeg()

            if vertexFound == False:
                arcsVertices.append(ArcVertice(int(edge.j), 0, 1, 0))


        else:
            arcs.append((int(edge.j),int(edge.i),edge.ji,999999, edge.ij))

            vertexFound = False
            for vertex in arcsVertices:
                if (vertex.name == int(edge.j)):
                    vertexFound = True
                    vertex.incOutdeg()

            if vertexFound == False:
                arcsVertices.append(ArcVertice(int(edge.j), 1, 0, 0))
            vertexFound = False
            for vertex in arcsVertices:
                if (vertex.name == int(edge.i)):
                    vertexFound = True
                    vertex.incIndeg()

            if vertexFound == False:
                arcsVertices.append(ArcVertice(int(edge.i), 0, 1, 0))

    print("3.(1) - complete")
    #----------------------------------------------------------------------------
    # 3.(2) - Construct digraph with cost flows
    arcsPrime = []
    for arc in arcs:
        arcij = (arc[0],arc[1],arc[2],arc[3])
        arcji = (arc[1],arc[0],arc[4],arc[3])
        arcart = (arc[1],arc[0],((arc[4] - arc[2]) / 2), 2) # the ''artificial arc''

        arcsPrime.append(arcij)
        arcsPrime.append(arcji)
        arcsPrime.append(arcart)

    for vertice in arcsVertices:
        vertice.recalcDemand()

    print("3.(2) - complete")
    #----------------------------------------------------------------------------
    # 3.(3) - Solve cost flow


    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
    
    for arc in arcsPrime:
        # Note: I think the arc[2] should not be an int! -> but float is not accepted here!?!
        print(arc)
        min_cost_flow.AddArcWithCapacityAndUnitCost(arc[0], arc[1], arc[3], int(arc[2] * 100))

    for vertice in arcsVertices:
        print("<<" + str(vertice.name) + "::" + str((-1) * vertice.demand) + ">>")
        min_cost_flow.SetNodeSupply(vertice.name, (-1) * vertice.demand)

    status = min_cost_flow.Solve()
    
    if status != min_cost_flow.OPTIMAL:
        print('There was an issue with the min cost flow input.')
        print(f'Status: {status}')
        exit(1)
    print('Minimum cost: ', min_cost_flow.OptimalCost())
    print('')
    print(' Arc   Flow / Capacity  Cost')

   
    print("3.(3) - complete")
    #----------------------------------------------------------------------------
    # 3.(4) - Construct another digraph and make an euler tour

    for i in range(min_cost_flow.NumArcs()):
        cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
        print('%1s -> %1s    %3s   / %3s   %3s' %
              (min_cost_flow.Tail(i), min_cost_flow.Head(i),
               min_cost_flow.Flow(i), min_cost_flow.Capacity(i), cost))

    arcsPrimePrime = []
    
    for i in range(2,min_cost_flow.NumArcs(),3):
        yij = min_cost_flow.Flow(i-2)
        yji = min_cost_flow.Flow(i-1)
        yart = min_cost_flow.Flow(i)

        if (yart == 0): # y_{ij}+1 copies of (i,j):
            arcsPrimePrime.append((min_cost_flow.Tail(i-2), min_cost_flow.Head(i-2)))
            for j in range(yij):
                arcsPrimePrime.append((min_cost_flow.Tail(i-2), min_cost_flow.Head(i-2)))
        else:
            arcsPrimePrime.append((min_cost_flow.Tail(i-1), min_cost_flow.Head(i-1)))
            for j in range(yji):
                arcsPrimePrime.append((min_cost_flow.Tail(i-1), min_cost_flow.Head(i-1)))
            
    for arc in arcsPrimePrime:
        print(arc)

    verticesPrime = []
    for arc in arcsPrimePrime:
        foundI = False
        foundJ = False

        for vertice in verticesPrime:
            if (arc[0] == vertice.name):
                foundI = True
                vertice.incOutdeg()
            if (arc[1] == vertice.name):
                foundJ = True
                vertice.incIndeg()
            if (foundI == True and foundJ == True):
                break
    
        if (foundI == False):
            verticesPrime.append(ArcVertice(arc[0], 1, 0, 0))
        if (foundJ == False):
            verticesPrime.append(ArcVertice(arc[1], 0, 1, 0))

    for vertice in verticesPrime:
        vertice.recalcDemand()
        if (vertice.demand != 0):
            print("DEMAND IS NOT 0, IT IS: " + str(vertice.demand))
    
    
    wpp_tour = (euler_tour(arcsPrimePrime, arcsPrimePrime[0][0]))
    return wpp_tour

def checkWpp(graph,wpp_tour):
    cost = 0

    edges = graph[1]
    edgeStack = copy.deepcopy(edges)

    if(wpp_tour[0] != wpp_tour[len(wpp_tour) - 1]):
        print("<<<<<CRITICAL-STARTING-POINT-IS-NOT-END-POINT - START: " + str(wpp_tour[0]) + "::END::" + str(wpp_tour[len(wpp_tour) - 1]))
    
    for index in range(1, len(wpp_tour)):
        i = wpp_tour[index-1]
        j = wpp_tour[index]

        edgeFound = False
        for edge in edges:
            if(int(edge.i) == i and int(edge.j) == j):
                cost = cost + edge.ij
                edgeFound = True
                break
            elif(int(edge.j) == i and int(edge.i) == j):
                cost = cost + edge.ji
                edgeFound = True
                break
        if (edgeFound == False):
            print("<<<<CRITICAL-EDGE-NOT-FOUND: " + str(i) + "::" + str(j))

        for edgeIndex in range(len(edgeStack)):
            if(int(edgeStack[edgeIndex].i) == i and int(edgeStack[edgeIndex].j) == j):
                edgeStack.pop(edgeIndex)
                break
            elif(int(edgeStack[edgeIndex].j) == i and int(edgeStack[edgeIndex].i) == j):
                edgeStack.pop(edgeIndex)
                break
    
    print("<<<<WPP-TOUR>>>>")
    print(wpp_tour)
    print("Total cost of: " + str(cost))


            
        

# Parse input file (file from args)
graph = parse_input_file()
isEulerian = is_eulerian(graph)
wpp_tour = None

if (isEulerian[0] == False):
    res_graph = to_eulerian_proc(graph, isEulerian[1])
    
    isEulerian = is_eulerian(res_graph)   
    if (isEulerian[0] == False):
        print("Cricital failure while converting to eulerian!")
        exit(1)
    
    wpp_tour = wins_algorithm(res_graph) 
   

else:
    wpp_tour = wins_algorithm(graph) 
    print("Graph is eulerian! - Starting eulerian solver")


checkWpp(graph,wpp_tour)



















