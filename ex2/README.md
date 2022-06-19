# Exercise 02

This repository contains our code related to the second exercise of PSSAI.

**Layout**

    .
    ├── instances                       --- WPP Problem sets
    ├── plots                           --- Some of the plots included in slides
    ├── plots_traces                    --- Cost traces of plots above
    ├── report                          --- Some visuals for the slides
    ├── solutions_from_known_best       --- Solutions using tours from previous exercise
    │   ├── tours                       
    │   │   └── costs
    │   └── traces
    ├── solutions_heuristic             --- Solutions using the greedy/heuristic initialisation
    │   ├── tours
    │   │   └── costs
    │   └── traces
    ├── solutions_random                --- Solutions using random initialisation
    │   ├── tours
    │   │   └── costs
    │   └── traces
    └── src                             --- Code for exercise
        └── figures                     --- Some more figures for slides



**Runing**

```
python3 start_all.py [-f tour] INSTANCE
```

where instance is one of the problems inside the `instances/` folder. This will create a cost history inside the `traces/` folder and the generated tour inside `tour/`.