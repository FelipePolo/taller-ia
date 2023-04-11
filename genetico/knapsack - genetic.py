import csv
import random
import time
from typing import List


class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


class Individual:
    def __init__(self, bits: List[int]):
        self.bits = bits
    
    def __str__(self):
        total_weight = sum([
            bit * item.weight
            for item, bit in zip(items, self.bits)
        ])
        return f"{self.bits} (Peso Mochila: {total_weight})"    

    def __hash__(self):
        return hash(str(self.bits))
    
    def fitness(self) -> float:
        total_value = sum([
            bit * item.value
            for item, bit in zip(items, self.bits)
        ])

        total_weight = sum([
            bit * item.weight
            for item, bit in zip(items, self.bits)
        ])

        if total_weight <= MAX_KNAPSACK_WEIGHT:
            return total_value
        
        return 0


MAX_KNAPSACK_WEIGHT = 7800
CROSSOVER_RATE = 0.53
MUTATION_RATE = 0.013
REPRODUCTION_RATE = 0.15

items = []

# Abrir el archivo CSV y leer los valores
with open('./input2.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=";")
    next(csv_reader) # Saltear la primera fila (etiquetas)

    # Leer los valores de la segunda y tercera columna de cada fila
    for row in csv_reader:
        name = row[0]
        value = int(row[1])
        weight = int(row[2])

        # Crear el objeto Item y agregarlo a la lista de items
        item = Item(name, weight, value)
        items.append(item)


def generate_initial_population(count=6) -> List[Individual]:
    population = set()

    # generate initial population having `count` individuals
    while len(population) != count:
        # pick random bits one for each item and 
        # create an individual 
        bits = [
            random.choice([0, 1])
            for _ in items
        ]
        population.add(Individual(bits))

    return list(population)


def selection(population: List[Individual]) -> List[Individual]:
    parents = []
    
    # randomly shuffle the population
    random.shuffle(population)

    # we use the first 4 individuals
    # run a tournament between them and
    # get two fit parents for the next steps of evolution

    # tournament between first and second
    if population[0].fitness() > population[1].fitness():
        parents.append(population[0])
    else:
        parents.append(population[1])
    
    # tournament between third and fourth
    if population[2].fitness() > population[3].fitness():
        parents.append(population[2])
    else:
        parents.append(population[3])

    return parents


def crossover(parents: List[Individual]) -> List[Individual]:
    N = len(items)

    child1 = parents[0].bits[:N//2] + parents[1].bits[N//2:]
    child2 = parents[0].bits[N//2:] + parents[1].bits[:N//2]

    return [Individual(child1), Individual(child2)]


def mutate(individuals: List[Individual]) -> List[Individual]:
    for individual in individuals:
        for i in range(len(individual.bits)):
            if random.random() < MUTATION_RATE:
                # Flip the bit
                individual.bits[i] = ~individual.bits[i]


def next_generation(population: List[Individual]) -> List[Individual]:
    next_gen = []
    while len(next_gen) < len(population):
        children = []

        # we run selection and get parents
        parents = selection(population)

        # reproduction
        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            # crossover
            if random.random() < CROSSOVER_RATE:
                children = crossover(parents)
            
            # mutation
            if random.random() < MUTATION_RATE:
                mutate(children)

        next_gen.extend(children)

    return next_gen[:len(population)]


def print_generation(population: List[Individual]):
    for individual in population:
        print(individual.bits, individual.fitness())
    print()
    print("Average fitness", sum([x.fitness() for x in population])/len(population))
    print("-" * 32)


def average_fitness(population: List[Individual]) -> float:
    return sum([i.fitness() for i in population]) / len(population)


def solve_knapsack() -> Individual:

    population = generate_initial_population()

    start_time = time.time()
    avg_fitnesses = []
    
    for i in range(500):
        avg_fitnesses.append(average_fitness(population))
        population = next_generation(population)
        if population[0].fitness() > 0:
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Tiempo empleado:", elapsed_time)
    print("Número de iteraciones:", i + 1)

    return population[0]


if __name__ == '__main__':
    for i in range(5):
        solution = solve_knapsack()
        print(solution)
        if solution.fitness() == 0:
            print("Solucion no apta - sobrepasa el peso permitido")
        else:
            print("Valor Total Mochila:"+str(solution.fitness()))   
    
        print()