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
    (bestSolL, bestSolD) = cloneSolutions(solL)

    if debug == True:
        print(bestSolCost)
        initialcost = bestSolCost[0][3]
        print('Initial cost is: ' + str(bestSolCost[0][3]))

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

    curBestSolCost = bestSolCost
    while (isInTime(startTime, maxTime) and c < maxIter):
        
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
                          
                if random.random() >= 0.5 and sol[2].getX() > 0:
                    op = "decX"
                    sol[2].decX()
                else:
                    op = "incX"
                    sol[2].incX()

                curCost = completeCost(solD, solL, graph[0], directedEdges, costDict, pathDict)
                regress = curCost[0][3] < curBestSolCost[0][3]

                d = curCost[0][3]-curBestSolCost[0][3]
                fr = d/T    
                exp = math.e**fr
                p = 1/(1+exp)

                if debug:
                    print(f"{curCost[0][3]} - {curBestSolCost[0][3]} = {d} | Exp: {exp} | p {p}")
                
                if regress:
                    fl.append(1)
                    curBestSolCost = curCost
                    (solL, solD) = cloneSolutions(solL)
                
                    al.append(curCost)
                    bl.append(curBestSolCost)
                    cl.append(d)
                    dl.append(exp)
                    el.append(p)

                    break
                elif random.random() < p:
                    fl.append(-1)
                    curBestSolCost = curCost
                    (solL, solD) = cloneSolutions(solL)
                    
                    al.append(curCost)
                    bl.append(curBestSolCost)
                    cl.append(d)
                    dl.append(exp)
                    el.append(p)

                    break
                else:
                    if op == "incX":
                        if (sol[2].getX() > 0):
                            sol[2].decX()                        
                    elif op =="decX":
                        sol[2].incX()
                        
               
            if curBestSolCost[0][3] < bestSolCost[0][3]:
                (bestSolL, bestSolD) = cloneSolutions(solL)
                bestSolCost = curBestSolCost 
                gl.append(bestSolCost)
                break

            i += 1

        if debug:
            print(f"Best {bestSolCost[0][3]} and inital {initialcost}")
            print()
        c = c + 1


    if debug:
        al2 = []
        bl2 = []
        gl2 = []

        for a in al:
            al2.append(a[0][3])

        for b in bl:
            bl2.append(b[0][3])

        for g in gl:
            gl2.append(g[0][3])

        fig, axs = plt.subplots(3,1)
        axs[0].plot(al2)
        axs[0].set_title("Current costs")
        axs[0].set_xlabel("Epochs")
        axs[0].set_ylabel("Score")
        axs[1].plot(bl2)
        axs[1].set_title("Current best costs")
        axs[1].set_xlabel("Epochs")
        axs[1].set_ylabel("Score")
        axs[2].plot(gl2)
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
        plt.savefig('hey.png')
        plt.show()
    
    if traceMode:
        write_trace_to_file(graph, gl, '_simulated_best')
        write_trace_to_file(graph, bl, '_simulated_all')

    bestSolCost = completeCost(bestSolD, bestSolL, graph[0], directedEdges, costDict, pathDict)

    return (bestSolD, bestSolL, bestSolCost)
