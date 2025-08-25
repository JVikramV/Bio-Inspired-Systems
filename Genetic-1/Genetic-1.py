import random

# -----------------------
# Function to optimize
# -----------------------
def fitness(x):
    return x ** 2   # we want to maximize this

# -----------------------
# GA Parameters
# -----------------------
POP_SIZE = 10        # number of individuals
GENS = 50            # number of generations
MUTATION_RATE = 0.1  # probability of mutation
CROSSOVER_RATE = 0.9 # probability of crossover
X_MIN, X_MAX = -10, 10  # search space

# -----------------------
# Create Initial Population
# -----------------------
def create_population():
    return [random.uniform(X_MIN, X_MAX) for _ in range(POP_SIZE)]

# -----------------------
# Selection (Roulette Wheel)
# -----------------------
def select(pop):
    fitnesses = [fitness(ind) for ind in pop]
    total_fit = sum(fitnesses)
    if total_fit == 0:  # avoid division by zero
        return random.choice(pop)
    probs = [f/total_fit for f in fitnesses]
    return random.choices(pop, weights=probs, k=1)[0]

# -----------------------
# Crossover (Single-point blend)
# -----------------------
def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        alpha = random.random()
        child = alpha * p1 + (1 - alpha) * p2
        return child
    return p1

# -----------------------
# Mutation
# -----------------------
def mutate(x):
    if random.random() < MUTATION_RATE:
        x += random.uniform(-1, 1)  # small change
        x = max(min(x, X_MAX), X_MIN)  # keep inside bounds
    return x

# -----------------------
# GA Main Loop
# -----------------------
def genetic_algorithm():
    population = create_population()
    best_solution = max(population, key=fitness)

    for g in range(GENS):
        new_population = []
        for _ in range(POP_SIZE):
            parent1 = select(population)
            parent2 = select(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        gen_best = max(population, key=fitness)
        if fitness(gen_best) > fitness(best_solution):
            best_solution = gen_best

        print(f"Generation {g+1}: Best = {gen_best:.4f}, Fitness = {fitness(gen_best):.4f}")

    print("\nBest solution found:")
    print(f"x = {best_solution:.4f}, f(x) = {fitness(best_solution):.4f}")

# -----------------------
# Run GA
# -----------------------
if __name__ == "__main__":
    genetic_algorithm()
