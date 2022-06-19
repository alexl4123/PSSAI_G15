import sys
import os
import time
import copy
import random
import math
import matplotlib.pyplot as plt

from src.graph_data_structs import *
from src.parse_input_file import parse_input_file
from src.hierholzer import euler_tour
from src.metasearch_common_procedures import * 
from src.metasearch_init_procedure import generalInitialization

def simmulated_annealing_algorithm(graph, inits, sols, maxTime=5, maxIter=100, traceMode=False, startTime=-1, debug=False):
    
    
    Tmax = 100
    r = 0.01
    Tmin = 10
    #debug = True


    (directedEdges, costDict, pathDict, verticesD, avgPerViolation) = inits
    (solL, solD) = sols

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    if debug == True:
        print(bestSolCost)
        initialcost = bestSolCost[0][3]
        print('Initial cost is: ' + str(bestSolCost[0][3]))

    if traceMode:
        trace = [bestSolCost]

    if startTime == -1:
        startTime = time.time()

    c = 0

    al = []
    bl = []
    cl = []
    dl = []
    el = []
    fl = []
    gl = []

    while (isInTime(startTime, maxTime) and c < maxIter):
        curBestSolCost = bestSolCost
        gl.append(bestSolCost[0][3])
        
        T = Tmax 
        i = 0
        while T >= Tmin:
            if not isInTime(startTime, maxTime):
                break

            # decrease temp (step 3)
            if debug:
                print(f"---- T: '{T}' --> '{Tmax * math.e**(-i*r)}'")
            T = Tmax * math.e**(-i*r)

            for sol in solL:
                if random.random() > 0.5:
                    op = "incX"
                    sol[2].incX()
                else:
                    op = "decX"
                    if (sol[2].getX() > 0):
                        sol[2].decX()

                curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
                regress = curCost[0][3] < curBestSolCost[0][3]

                d = curCost[0][3]-curBestSolCost[0][3]
                fr = 1/((d/T)+1)   
                exp = math.e**fr
                p = 1/(1+exp)

                if debug:
                    print(f"{curCost[0][3]} - {curBestSolCost[0][3]} = {d} | Exp: {exp} | p {p}")
            
                if traceMode:
                    trace.append(curBestSolCost)

                if regress:
                    fl.append(1)
                    curBestSolCost = curCost
                elif random.random() < p:
                    fl.append(-1)
                    curBestSolCost = curCost
                    bestSolCost = curBestSolCost

                if op == "incX":
                    if (sol[2].getX() > 0):
                        sol[2].decX()                        
                elif op =="decX":
                    sol[2].incX()
                else:
                    continue
                
            
            al.append(curCost[0][3])
            bl.append(curBestSolCost[0][3])
            cl.append(d)
                
            if curBestSolCost[0][3] < bestSolCost[0][3]:
                (solL, solD) = cloneSolutions(solL)
                bestSolCost = curBestSolCost
                break

            i += 1

        if debug:
            print(f"Best {bestSolCost[0][3]} and inital {initialcost}")
            print()
        c = c + 1


    if debug:
        fig, axs = plt.subplots(3,1)
        axs[0].plot(al)
        axs[0].set_title("Current costs")
        axs[0].set_xlabel("Epochs")
        axs[0].set_ylabel("Score")
        axs[1].plot(bl)
        axs[1].set_title("Current best costs")
        axs[1].set_xlabel("Epochs")
        axs[1].set_ylabel("Score")
        axs[2].plot(gl)
        axs[2].set_title("Best cost")
        axs[2].set_xlabel("Epochs")
        axs[2].set_ylabel("Score")
        #axs[2].plot(cl)
        #axs[2].set_title("diff")
        #axs[3].plot(dl)
        #axs[3].set_title("exp")
        #axs[4].plot(el)
        #axs[4].set_title("p")
        #axs[5].scatter([i for i in range(len(fl))], fl)
        #axs[5].set_title("regress/annealing")
        plt.tight_layout()
        plt.show()
    

    bestSolCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
    (solL, solD) = cloneSolutions(solL)
    
    if not traceMode:
        return (solD, solL, bestSolCost)
    else:
        return (solD, solL, bestSolCost, trace)
