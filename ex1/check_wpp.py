# coding=utf-8
import sys
import time
import copy
import ast


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

    if (total != 3):
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

    input_file_path = sys.argv[2]
    input_file = open(input_file_path, "r")
    list_ = input_file.readline()
    input_file.close()

    list_ = ast.literal_eval(list_)

       
    
    return (vertices, edgeList, list_)



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

graph = parse_input_file()
checkWpp((graph[0], graph[1]),graph[2])
