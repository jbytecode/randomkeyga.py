# randomkeyga.py

Random Key Genetic Algorithm for Permutation Based Optimization Problems in Python


## Example 


Here is a simple traveling salesman problem.

First things first:

```python 
from randomkeyga import optimizer
```


Coordinates of the points to visit:

```python
points = [
        [0, 0], [0, 1], [0, 2],
        [1, 2], [2, 2], [3, 2],
        [3, 1], [3, 0], [2, 0], [1, 0]
    ]
```

The Euclidean distance function (Numpy can be used instead for faster calculation)

```python
def distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5 
```

The objective function. The total distance will be minimized:

```python 
def total_distance(path):
    total = 0
    for i in range(len(path)-1):
        total += distance(points[path[i]], points[path[i+1]])
    # Add the distance from the last point to the first point
    total += distance(points[path[-1]], points[path[0]])
    return total

```

Optimize:


```python
result = optimizer.optimize(
            popsize=100,
            chsize=10,
            costfunction=total_distance,
            selection_operator=optimizer.TournamentSelection(2),
            crossover_operator=optimizer.OnePointCrossOver(),
            mutation_operator=optimizer.RandomMutation(0.01),
            crossover_rate=crossover_rate,
            mutation_rate=0.01,
            elitism=2,
            generations=200)

best = result.chromosomes[0]
```

Currently only the `TournamentSelection` is implemented as the selection operator. 
`OnePointCrossOver`, `TwoPointCrossOver`, and `UniformCrossOver` are alternative recombination operators.
`RandomMutation` is the implemented mutation operator. 