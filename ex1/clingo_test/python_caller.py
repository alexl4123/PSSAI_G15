import os

from parse_input_file import *


read = parse_input_file()

output_file_path = 'tmp.lp'

f = open(output_file_path, 'w')

for vertice in read[0]:
    f.write('v(' + str(vertice.name) + ').\n')

for vertice in read[0]:
    for edge in vertice.getEdges():
        f.write('c(' + str(edge.i) + ',' + str(edge.j) + ',' + str(edge.ij) + ').\n')
        f.write('c(' + str(edge.j) + ',' + str(edge.i) + ',' + str(edge.ji) + ').\n')

f.close()   

done = False
while done == False:
    # Invoke polynomial solver of minimum-cost-perfect-matching
    stream = os.popen('clingo --model 1 clingo_test.lp ' + output_file_path)
    output = stream.read()


    if 'totalcost(' in output:
        outputs = output.split('totalcost(')
        value = int((outputs[1].split(')'))[0])

        print('New best val found: ' + value)

        f = open(output_file_path, 'a')
        f.write(':- totalcost(C), C >= ' + str(value) + '.\n')
        f.close()

    else:
        done = True
        print(output)
        print('Best val: ' + str(value))


