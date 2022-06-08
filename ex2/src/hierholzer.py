
def euler_tour(arcsPrimePrime, startNode):
    arcsStack = (arcsPrimePrime)
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
                    curStack = [tour.pop(i)] + curStack
                else:
                    curCurNode = tour[i]
                    tour.pop(i)
                    curStack = euler_tour(arcsStack, curCurNode) + curStack
            """
            print("<<<<<<<<<<Start node: " + str(startNode) + ">>>>>>>>>>>>")
            print(arcsStack)
            print(tour)
            print(curStack)
            print("<<<<<<<<<<>>>>>>>>>>")
            """
 
            return (tour + curStack)
    
    """
    print("<<<<<<<<<<Start node: " + str(startNode) + ">>>>>>>>>>>>")
    print(tour)
    print(curNode)
    print("<<<<<<<<<<>>>>>>>>>>")
    """
    return tour


