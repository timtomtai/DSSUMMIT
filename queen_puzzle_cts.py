import random

def random_chromosome():
    #randomly  allocated values
    return [ random.randint(0, 7 ) for _ in range(8) ]

def fitness(chromosome):
    #check the fitness of a chromosome / an iteration
    horizontal_collisions = sum([chromosome.count(q)-1 for q in chromosome])/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))



def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Not here"

def reproduce(x, y):
    #cross_over
    c = random.randint(0, 7)
    return x[0:c] + y[c:8]

def mutate(x):
    #randomly changing the value of a random index of a chromosome

    c = random.randint(0, 7)
    m = random.randint(0, 7)
    x[c] = m
    return x

def genetic_queen(population, fitness, generation):
    mutation_probability = 0.05
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child, generation)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population

def print_chromosome(chrom, generation):
    print("Generation = {} Chromosome = {}  Fitness = {}"
        .format(generation, str(chrom), fitness(chrom)))

if __name__ == "__main__":

    maxFitness = 28
    population = [random_chromosome() for _ in range(100)]

    generation = 1

    while not maxFitness in [fitness(chrom) for chrom in population]:

        population = genetic_queen(population, fitness, generation)
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    chrom_out = []

    for chrom in population:
        if fitness(chrom) == maxFitness:
            print("One of the solutions : ")
            chrom_out = chrom
            print_chromosome(chrom,generation-1)
