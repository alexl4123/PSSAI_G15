
class Edge:
    def __init__(self, i, j, ij, ji):
        self.i = i
        self.j = j
        self.ij = ij
        self.ji = ji

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

class DirectedEdge:
    def __init__(self, i, j, cost):
        self.i = i
        self.j = j
        self.cost = cost

    def show(self):
        string = '(' + str(self.i) + ',' + str(self.j) + ') = ' + str(cost)
        return string


class SolutionRepresentation:
    def __init__(self, cost):
        self._x = 0
        self._cost = cost

    def incX(self):
        self._x = self._x + 1

    def decX(self):
        self._x = self._x - 1
        
    def reset(self):
        self._x = 0

    def set(self, number):
        self._x = number

    def cost(self):
        return (self._cost * self._x)

    def singleCost(self):
        return self._cost

    def getX(self):
        return self._x

    def clone(self):
        new = SolutionRepresentation(self._cost)
        new._x = self._x

        return new










