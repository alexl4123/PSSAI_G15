import os
import sys
import time

path = "instances/"
files = (os.listdir(path))

for fp in files:
    f = open(path + fp, 'rb')
    lines = f.readlines()
    f.close()
    f = open(path + fp, 'wb')
    for lineIndex in range(len(lines) - 1):
        f.write(lines[lineIndex])
    f.close()
    
