# WINDY_POSTMAN_PROBLEM (WPP) - PSSAI_G15

## General things that can be found here:

In exercise 1 an implementation of the ''Win's algorithm'' was made, which is a heuristic algorithm for the WPP. In exercise 2 we explored various Meta-Heuristics (Genetic Algorithms Simulated Annealing, plain old Local Search) for WPP. 

In general this was a small project for a class in the Summer Term 2022.

## Group Details

Problem Solving and Search in Artificial Intelligence - Group 15

Exercise 1 and 2.



# What can be found here

For **exercise 2** consult the README.md in **PSSAI_G15/ex2/README.md**, for **exercise 1 read on**.

# What can be found here?

- Win's algorithm: 'ex1/wins_algorithm.py'
    - Can be called by (asusming one is in folder ex1): ./wins_algorithm.py instances/<INSTANCE>
    - E.g. ./wins_algorithm.py instances/toy
    - Might NOT work on windows (due to the efficient solver for the Minimum-Cost-Perfect-Matching
    - The resulting tour can be found in 'ex1/tours'
    - The resulting euler graph can be found in 'ex1/eulerian' 
        - Note that if an eulerian graph is already present for an instance it is used
- Naive algorithm: 'ex1/naive.py'
    - Can be called by (asusming one is in folder ex1): ./naive.py instances/<INSTANCE>
    - E.g. ./naive.py instances/toy
    - The resulting tour can be found in 'ex1/tours' with the ending '_naive_tour'
- The script 'ex1/all_sols.sh' executes all instances for the 'wins_algorithm.py'
- The script 'ex1/all_sols_naive.sh' executes all instances for the 'naive.py' (Will get stuck after 6 instances)
- The folder 'ex1/mcpm' contains the efficient implementation of the Mininmum-Cost-Perfect-Matching algorithm found on GitHub (https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching)
- Check if a tour is a WP-Tour and get it's cost: 'check_wpp.py'
    - Can be called by (assuming one is in folder ex1): ./check_wpp.py instances/<INSTANCE> tours/<TOUR>
    - E.g. ./check_wpp.py instances/toy tours/toy_tour
- Find eulerian tour on directed graph: 'hierholzer.py'
    - CANNOT be called direclty, one must call the function in there
- Other files are for logs/submission paper only


