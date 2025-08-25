import random
import math

# =====================================
# TSP setup
# =====================================
# Example cities (x, y coordinates)
cities = {
    0: (0, 0),
    1: (1, 5),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3),
    5: (2, 7)
}
NUM_CITIES = len(cities)

# Distance function
def distance(a, b):
    (x1, y1), (x2, y2) = cities[a], cities[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Total path length
def total_distance(tour):
    return sum(distance(tour[i], tour[(i+1) % NUM_CITIES]) for i in range(NUM_CITIES))

# =====================================
# GEA parameters
# =====================================
POP_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8

# =====================================
# Genetic Operations
# =====================================
def initialize_population():
    population = []
    for _ in range(POP_SIZE):
        tour = list(range(NUM_CITIES))
        random.shuffle(tour)
        population.append(tour)
    return population

def fitness(tour):
    return 1 / total_distance(tour)

def selection(population):
    # Tournament selection
    k = 3
    selected = random.sample(population, k)
    return min(selected, key=total_distance)

def crossover(parent1, parent2):
    if random.random() > CROSSOVER_RATE:
        return parent1[:]
    start, end = sorted(random.sample(range(NUM_CITIES), 2))
    child = [None] * NUM_CITIES
    # Copy slice from parent1
    child[start:end] = parent1[start:end]
    # Fill remaining with parent2 order
    p2_seq = [gene for gene in parent2 if gene not in child]
    j = 0
    for i in range(NUM_CITIES):
        if child[i] is None:
            child[i] = p2_seq[j]
            j += 1
    return child

def mutate(tour):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(NUM_CITIES), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

# =====================================
# Main Evolution Loop
# =====================================
population = initialize_population()
best_solution = min(population, key=total_distance)

for gen in range(GENERATIONS):
    new_population = []
    while len(new_population) < POP_SIZE:
        p1, p2 = selection(population), selection(population)
        child = crossover(p1, p2)
        child = mutate(child)
        new_population.append(child)

    population = new_population
    current_best = min(population, key=total_distance)
    if total_distance(current_best) < total_distance(best_solution):
        best_solution = current_best

    print(f"Gen {gen+1}: Best Distance = {total_distance(best_solution):.4f}")

# =====================================
# Final Result
# =====================================
print("\nBest tour found:", best_solution)
print("Best distance:", total_distance(best_solution))
