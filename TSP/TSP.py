import random
import math

# ---------------------------
# 1. City coordinates
# ---------------------------
cities = {
    0: (0, 0),
    1: (2, 6),
    2: (5, 4),
    3: (6, 1),
    4: (8, 7)
}

NUM_CITIES = len(cities)

# ---------------------------
# 2. Distance function
# ---------------------------
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# ---------------------------
# 3. Total route distance
# ---------------------------
def route_distance(route):
    total = 0
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)] 
        total += distance(current_city, next_city)
    return total

# ---------------------------
# 4. Create initial population
# ---------------------------
def create_population(pop_size):
    population = []
    base_route = list(cities.keys())
    for _ in range(pop_size):
        individual = base_route[:]
        random.shuffle(individual)
        population.append(individual)
    return population

# ---------------------------
# 5. Fitness function
# ---------------------------
def fitness(route):
    return 1 / route_distance(route)

# ---------------------------
# 6. Selection (tournament)
# ---------------------------
def selection(population, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda route: route_distance(route))
    return selected[0]

# ---------------------------
# 7. Crossover (ordered crossover)
# ---------------------------
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end+1] = parent1[start:end+1]

    pointer = 0
    for city in parent2:
        if city not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = city

    return child

# ---------------------------
# 8. Mutation (swap mutation)
# ---------------------------
def mutate(route, mutation_rate=0.1):
    route = route[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# ---------------------------
# 9. Genetic Algorithm
# ---------------------------
def genetic_algorithm(pop_size=5, generations=10, mutation_rate=0.1):
    population = create_population(pop_size)

    best_route = min(population, key=route_distance)
    best_distance = route_distance(best_route)

    for generation in range(generations):
        new_population = []

        for _ in range(pop_size):
            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            new_population.append(child)

        population = new_population

        current_best = min(population, key=route_distance)
        current_distance = route_distance(current_best)

        print(f"Generation {generation+1}: Current Best  = {current_distance:.2f}")
        print(f"Generation {generation+1}: Best Distance = {best_distance:.2f}")

        if current_distance < best_distance:
            best_route = current_best
            best_distance = current_distance

    

    return best_route, best_distance

# ---------------------------
# 10. Run
# ---------------------------
best_route, best_distance = genetic_algorithm()

print("\nBest route found:", best_route)
print("Best distance:", round(best_distance, 2))