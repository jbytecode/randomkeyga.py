import numpy as np 

class Chromosome:
    def __init__(self, chsize: int):
        # Chromosome size
        self.chsize = chsize
        
        # Chromosome values are random float values between 0 and 1
        self.realdata = np.random.rand(chsize)
        
        # Default cost value is maximum float value
        self.cost = float('inf')


    def decode(self)-> np.ndarray:
        # Decode chromosome values to integer values
        return np.argsort(self.realdata)
    
    def __str__(self):
        return f"Chromosome: {np.argsort(self.realdata)}, Cost: {self.cost}"
    
    def __repr__(self):
        return f"Chromosome: {np.argsort(self.realdata)}, Cost: {self.cost}"


class Population:
    def __init__(self, popsize: int, chsize: int, costfunction: callable):
        # Population size
        self.popsize = popsize
        
        # Chromosome size
        self.chsize = chsize
        
        # Cost function
        self.costfunction = costfunction
        
        # Create population
        self.chromosomes = [Chromosome(chsize) for _ in range(popsize)]
        

    def sort(self):
        # Sort population by fitness values
        self.chromosomes.sort(key=lambda x: x.cost)

    def calculate_costs(self):
        # Calculate cost values for each chromosome
        for chromosome in self.chromosomes:
            chromosome.cost = self.costfunction(chromosome.decode())

    def get_best(self) -> Chromosome:
        # First sort the population
        self.sort()

        # Get best chromosome
        return self.chromosomes[0]
    

class CrossoverOperator:
    def __init__(self):
        pass

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        pass 



class OnePointCrossOver(CrossoverOperator):
    def __init__(self):
        super().__init__()

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        # Create a new chromosome
        child = Chromosome(parent1.chsize)

        # Select a random crossover point
        crossover_point = np.random.randint(0, parent1.chsize)

        # Copy the first part of the chromosome from parent1
        child.realdata[:crossover_point] = parent1.realdata[:crossover_point]

        # Copy the second part of the chromosome from parent2
        child.realdata[crossover_point:] = parent2.realdata[crossover_point:]

        return child
    
class TwoPointCrossOver(CrossoverOperator):
    def __init__(self):
        super().__init__()

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        # Create a new chromosome
        child = Chromosome(parent1.chsize)

        # Select two random crossover points
        crossover_points = np.random.choice(range(parent1.chsize), 2, replace=False)
        crossover_points.sort()

        # Copy the first part of the chromosome from parent1
        child.realdata[:crossover_points[0]] = parent1.realdata[:crossover_points[0]]

        # Copy the second part of the chromosome from parent2
        child.realdata[crossover_points[0]:crossover_points[1]] = parent2.realdata[crossover_points[0]:crossover_points[1]]

        # Copy the third part of the chromosome from parent1
        child.realdata[crossover_points[1]:] = parent1.realdata[crossover_points[1]:]

        return child
    

class UniformCrossOver(CrossoverOperator):
    def __init__(self):
        super().__init__()

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        # Create a new chromosome
        child = Chromosome(parent1.chsize)
        # Randomly select which genes to copy from parent1 and parent2
        child.realdata = np.where(np.random.randint(0, 2, parent1.chsize), parent1.realdata, parent2.realdata)
        return child
    

class MutationOperator:
    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        pass


class RandomMutation(MutationOperator):
    def __init__(self, mutation_rate: float):
        super().__init__(mutation_rate)

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        # Create a new chromosome
        mutated_chromosome = Chromosome(chromosome.chsize)

        # Copy the chromosome values
        mutated_chromosome.realdata = chromosome.realdata.copy()

        # Randomly change some genes
        for i in range(chromosome.chsize):
            if np.random.rand() < self.mutation_rate:
                mutated_chromosome.realdata[i] = np.random.rand()

        return mutated_chromosome
    

class SelectionOperator:
    def __init__(self):
        pass

    def select(self, population: Population) -> Chromosome:
        pass

class TournamentSelection(SelectionOperator):
    def __init__(self, tournament_size: int):
        super().__init__()
        self.tournament_size = tournament_size

    def select(self, population: Population) -> Chromosome:
        # Randomly select tournament_size chromosomes
        tournament: np.ndarray = np.random.choice(population.chromosomes, self.tournament_size, replace=False)

        # Sort the tournament
        tournament = list(tournament)
        list(tournament).sort(key=lambda x: x.cost)
        
        # Return the best chromosome
        return tournament[0]
    

def generation(pop: Population, 
               selection_operator: SelectionOperator,
               crossover_operator: CrossoverOperator,
               mutation_operator: MutationOperator,
                crossover_rate: float,
                mutation_rate: float,
                elitism: int) -> Population:
    
    # Population size 
    popsize = len(pop.chromosomes)

    # Chromosome size 
    chsize = pop.chromosomes[0].chsize

    # Create a new population
    new_pop = Population(popsize, chsize, pop.costfunction)

    # Calculate costs
    pop.calculate_costs()

    # Sort the population
    pop.sort()

    # Elitism
    for i in range(elitism):
        new_pop.chromosomes[i] = pop.chromosomes[i]

    # Add new chromosomes to the new population greedily
    for i in range(elitism, popsize):
        # Select parents
        parent1 = selection_operator.select(pop)
        parent2 = selection_operator.select(pop)

        # Crossover
        if np.random.rand() < crossover_rate:
            child = crossover_operator.crossover(parent1, parent2)
        else:
            child = parent1

        # Mutation
        if np.random.rand() < mutation_rate:
            child = mutation_operator.mutate(child)

        # Add the child to the new population
        new_pop.chromosomes[i] = child

    return new_pop

def optimize(popsize: int, chsize: int, costfunction: callable, 
             selection_operator: SelectionOperator, crossover_operator: CrossoverOperator, 
             mutation_operator: MutationOperator, crossover_rate: float, mutation_rate: float, elitism: int, generations: int, verbose=True) -> Population:
    
    # Create a population
    pop = Population(popsize, chsize, costfunction)

    # Optimize
    for i in range(generations):
        pop = generation(pop, selection_operator, crossover_operator, mutation_operator, crossover_rate, mutation_rate, elitism)
        if verbose:
            print(pop.chromosomes[0])
            
    # Calculate costs and sort by costs 
    pop.sort()

    # Return the entire population after the optimization
    return pop