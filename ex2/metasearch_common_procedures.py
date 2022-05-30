# coding=utf-8
import sys
import os
import time
import copy
import random

from graph_data_structs import *
from hierholzer import euler_tour

# ------------------------------------------------------------------------------------
# - Some Helper Functions                                                            -
# ------------------------------------------------------------------------------------

def validInit(solL):
    for sol in solL:
        sol[2].incX()

def randomizedInit(solL):
    for sol in solL:
        sol[2].reset()
        randNum = random.randint(0,1)
        if randNum == 1:
            sol[2].incX()

def initSolutions(directedEdges):
    solL = []
    solD = {}

    for edge in directedEdges:
        curSol = SolutionRepresentation(edge.cost)
        solL.append((edge.i,edge.j,curSol))
        solD[str(edge.i) + ':' +str(edge.j)] = curSol
    
    return(solL, solD)

def cloneSolutions(solL):
    newSolL = []
    newSolD = {}

    for sol in solL:
        newSol = sol[2].clone()
        newSolL.append((sol[0], sol[1], newSol))
        newSolD[str(sol[0]) + ':' + str(sol[1])] = newSol

    return (newSolL, newSolD)

def validWpp(vertices, edges, solD):

    for edge in edges:
        s = solD[str(edge.i) + ':' + str(edge.j)].getX() + solD[str(edge.j) + ':' + str(edge.i)].getX()
        if (s != 2):
            print('<<Constraint Violation found for: (' + str(edge.i) + str(edge.j) + ')')

    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if vertex.name == edge.i:
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
            else:
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()

        if (s != 0):
            print('<#<Constraint Violation found for vertex: (' + str(vertex.name) +  ')')

# prevCosts: (Basic Costs, CS2 Costs, CS3 Costs, Total Costs)
# changed: (v1, v2, diff)
def iterativeCost(solD, solL, verticesD, prevCosts, changed, avgCs3Cost):
    (ps, pcs2, pcs3, ptotal) = prevCosts[0]

    changedSol = solD[str(changed[0]) + ':' + str(changed[1])]
    revChangedSol = solD[str(changed[1]) + ':' + str(changed[0])]

    # Basic Cost update
    ps = ps + (changed[2] * changedSol.singleCost())

    # CS2 Cost update
    if ((changedSol.getX() + revChangedSol.getX()) == 0):
        pcs2 = pcs2 + changedSol.singleCost() + revChangedSol.singleCost()

    # CS3 Cost update (first part)
    vertices = [verticesD[str(changed[0])], verticesD[str(changed[1])]]
    violationsAfter = 0
    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if str(vertex.name) == str(edge.i):
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
                s = s - solD[str(edge.j) + ':' + str(edge.i)].getX()
            else:
                s = s + solD[str(edge.j) + ':' + str(edge.i)].getX()
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()
        violationsAfter = violationsAfter + abs(s) 

    # CS3 Cost update (second part)
    if changed[2] < 0:
        for i in range(0,abs(changed[2])):
            changedSol.incX()
    else:
        for i in range(0,abs(changed[2])):
            changedSol.decX()

    vertices = [verticesD[str(changed[0])], verticesD[str(changed[1])]]
    violationsBefore = 0
    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if str(vertex.name) == str(edge.i):
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
                s = s - solD[str(edge.j) + ':' + str(edge.i)].getX()
            else:
                s = s + solD[str(edge.j) + ':' + str(edge.i)].getX()
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()
        violationsBefore = violationsBefore + abs(s) 

    if changed[2] < 0:
        for i in range(0,abs(changed[2])):
            changedSol.decX()
    else:
        for i in range(0,abs(changed[2])):
            changedSol.incX()

    # CS3 Cost update (final part)
    
    pcs3 = pcs3 + (violationsAfter - violationsBefore) * avgCs3Cost * 0.1
    if pcs3 < 0 :
        pcs3 = 0

    return ((ps, pcs2, pcs3, (ps + pcs2 + pcs3)), [], [])

def completeCost(solD, solL, vertices, edges, costDict, pathDict):
   
    # Basic Costs
    costsTraversals = 0
    for sol in solL:
        costsTraversals = costsTraversals + sol[2].cost()

    # CS2 Costs
    cs2Costs = 0
    cs2Errors = []

    for edge in edges:
        s = solD[str(edge.i) + ':' + str(edge.j)].getX() + solD[str(edge.j) + ':' + str(edge.i)].getX()
        if s == 0:
            cs2Costs = cs2Costs + solD[str(edge.i) + ':' + str(edge.j)].singleCost() + solD[str(edge.j) + ':' + str(edge.i)].singleCost()
            cs2Errors.append((str(edge.i), str(edge.j)))
            cs2Errors.append((str(edge.j), str(edge.i)))
    
    # -------------------------------------------------------------------------------
    # CS3 Costs
    cs3Costs = 0
    cs3Errors = []
    eNegCs3Errors = []
    ePosCs3Errors = []

    cs3VerticesAmount = 0

    usedVertices = {}

    for vertex in vertices:
        s = 0
        for edge in vertex.getEdges():
            if str(vertex.name) == str(edge.i):
                s = s + solD[str(edge.i) + ':' + str(edge.j)].getX()
                s = s - solD[str(edge.j) + ':' + str(edge.i)].getX()
            else:
                s = s + solD[str(edge.j) + ':' + str(edge.i)].getX()
                s = s - solD[str(edge.i) + ':' + str(edge.j)].getX()
        
        if s < 0:
            for i in range(0,abs(s)):
                eNegCs3Errors.append((vertex.name, cs3VerticesAmount))
                usedVertices[cs3VerticesAmount] = vertex.name
                cs3VerticesAmount = cs3VerticesAmount + 1
        elif s > 0:
            for i in range(0,abs(s)):
                ePosCs3Errors.append((vertex.name, cs3VerticesAmount))
                usedVertices[cs3VerticesAmount] = vertex.name
                cs3VerticesAmount = cs3VerticesAmount + 1

    if len(eNegCs3Errors) > 0 or len(ePosCs3Errors) > 0:
        # If Constraint 3 is violated, compute perfect matching between those violations in terms of minimum repair cost

        mcpm = []

        for neg in eNegCs3Errors:
            for pos in ePosCs3Errors:
                mcpm.append((int(neg[1]), int(pos[1]), costDict[str(neg[0]) + ':' + str(pos[0])]))
            
        mcpm_path = '../ex1/mcpm'
        input_file_path = mcpm_path + '/tmp'

        f = open(input_file_path, 'w')
        
        f.write(str(cs3VerticesAmount) + "\n")
        f.write(str(len(mcpm)) + "\n")

        for pair in mcpm:
            f.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(pair[2]) + '\n')

        f.close()   
        
        # Invoke polynomial solver of minimum-cost-perfect-matching
        stream = os.popen(mcpm_path + '/example -f ' + input_file_path + ' --minweight')
        output = stream.read()

        lines = output.splitlines()
        for index in range(len(lines)):
            if index == 0:
                line = lines[index]
                splits = line.split(' ')
                cs3Costs = cs3Costs + (int(splits[len(splits) - 1]))
            elif index == 1:
                pass
            else:
                line = lines[index]
                splits = line.split(' ')

                cs3Errors.append((usedVertices[int(splits[0])], usedVertices[int(splits[1])]))

    return ((costsTraversals, cs2Costs, cs3Costs, (costsTraversals + cs2Costs + cs3Costs)), cs2Errors, cs3Errors, cs3VerticesAmount)


