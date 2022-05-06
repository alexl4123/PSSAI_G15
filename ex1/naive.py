# coding=utf-8
"""OR-Tools solution to the N-queens problem."""
import sys
import time
from ortools.sat.python import cp_model

from hierholzer import *

class Edge:
    def __init__(self, i, j, ij, ji):
        self.i = i
        self.j = j
        self.ij = ij
        self.ji = ji

def create_data_model():
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

    matrix = []
    for x in input_file:
        if (x[0] == '('):
            parse_input_line(x, matrix)

    input_file.close()

    data = matrix
    return data


"""
class NQueenSolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, queens):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution %i, time = %f s' %
              (self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1

        all_queens = range(len(self.__queens))
        for i in all_queens:
            for j in all_queens:
                if self.Value(self.__queens[j]) == i:
                    # There is a queen in column j, row i.
                    print('Q', end=' ')
                else:
                    print('_', end=' ')
            print()
        print()
"""


def main():
    # Creates the solver.
    model = cp_model.CpModel()

    edges = create_data_model()
    #edges.append(Edge('A','B',5,6))

    # Creates the variables.
    # cs0-begin Adds constraint xij, xji >= 0
    x = []
    for edge in edges:
        x.append(Edge(edge.i, edge.j,  model.NewIntVar(0, 2, 'x' + edge.i + edge.j), model.NewIntVar(0, 2, 'x' + edge.j + edge.i)))
    # cs0-end


    # cs1-begin: Adds constraint xij + xji >= 1
    for edge in x:
        model.Add(edge.ij + edge.ji >= 1)
    # cs1-end

    # Adds constraint (closed walk)
    # cs2-begin
    vertices = []
    for edge in edges:
        vertices.append(edge.i)
        vertices.append(edge.j)

    vertices = set(vertices)
    for vertice in vertices:
        cs = 0
        for edge in x:
            if (edge.i == vertice):
                cs = cs + edge.ij - edge.ji
                # print(vertice + ':' + edge.i  + ' - ' + edge.j)
            elif (edge.j == vertice):
                cs = cs + edge.ji - edge.ij
                # print(vertice + ':' + edge.j  + ' - ' + edge.i)

        model.Add(cs == 0)
    # cs2-end 
   
    # cs3-begin Adds Minimization constraint
    s = 0
    for i in range(0,len(edges)):
        s = s + x[i].ij * edges[i].ij
        s = s + x[i].ji * edges[i].ji

    model.Minimize(s) # minimize: x0ij * c0ij + x1ji ... + xnji * cnji
    # cs3-end

    # Solve the model.
    solver = cp_model.CpSolver()
    #solution_printer = NQueenSolutionPrinter(queens)
    #solver.parameters.enumerate_all_solutions = True
    #solver.Solve(model, solution_printer)
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Minimum of objective function: {solver.ObjectiveValue()}\n')
        for edge in x:
            print('For edge ' + edge.i + ':' + edge.j + ' we got (ij):' + str(solver.Value(edge.ij)) + ' and (ji):' + str(solver.Value(edge.ji)))

        solverValuesCopy = []
        for edge in x:
            for i in range(0, solver.Value(edge.ij)):
                solverValuesCopy.append((int(edge.i), int(edge.j)))
            for i in range(0, solver.Value(edge.ji)):
                solverValuesCopy.append((int(edge.j), int(edge.i)))

        wpp_tour = euler_tour(solverValuesCopy.copy(), solverValuesCopy[0][0])
        print("<<<<<<POSSIBLE_TOUR>>>>>>>>>>>")
        print(wpp_tour)
        print("<<<<<<POSSIBLE_TOUR_END>>>>>>>>>>>")

        input_file_path = sys.argv[1]
        input_file_name = input_file_path.split('/')

        input_file_name = input_file_name[len(input_file_name) - 1]
    
        output_file_path = 'tours/' + input_file_name + '_naive_tour'

        f = open(output_file_path, 'w')
    
        f.write(str(wpp_tour) + '\n')

        f.close()
                
    else:
        print('No solution found')
    # Statistics.
    print('\nStatistics')
    print(f'  status         : {solver.StatusName(status)}')
    print(f'  conflicts      : {solver.NumConflicts()}')
    print(f'  branches       : {solver.NumBranches()}')
    print(f'  wall time      : {solver.WallTime()} s')
    # print(f'  solutions found: {solution_printer.solution_count()}')


if __name__ == '__main__':
    main()





