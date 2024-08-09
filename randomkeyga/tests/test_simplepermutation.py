from randomkeyga import optimizer


def test_simple_permutation():
    
    # Define the points for the traveling salesman problem
    # The points are in the order of the path
    # The path is a cycle that starts and ends at the first point
    # 
    # 2 3 4 5
    # 1     6
    # 0 9 8 7
    # The distances between the points are 1 for all pairs 
    # so the total distance is 10
    points = [
        [0, 0], [0, 1], [0, 2],
        [1, 2], [2, 2], [3, 2],
        [3, 1], [3, 0], [2, 0], [1, 0]
    ]

    # Calculate the distance between points (Euclidean distance)
    def distance(point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    
    # Calculate the total distance of a given path
    def total_distance(path):
        total = 0
        for i in range(len(path)-1):
            total += distance(points[path[i]], points[path[i+1]])
        # Add the distance from the last point to the first point
        total += distance(points[path[-1]], points[path[0]])
        return total
    
    # optimize traveling salesman problem
    popsize = 100
    chsize = 10
    crossover_rate = 0.9
    mutation_rate = 0.1

    # optimize 10 times and get the best result
    hasfound = False
    for i in range(5):
        result = optimizer.optimize(
            popsize=popsize,
            chsize=chsize,
            costfunction=total_distance,
            selection_operator=optimizer.TournamentSelection(2),
            crossover_operator=optimizer.OnePointCrossOver(),
            mutation_operator=optimizer.RandomMutation(mutation_rate),
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            elitism=2,
            generations=200)
        best = result.chromosomes[0]
        if best.cost == 10:
            hasfound = True 
            break

    assert hasfound == True

if __name__ == "__main__":
    test_simple_permutation()
