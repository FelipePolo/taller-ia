import csv
import random
import time
from Item import Item
from Individual import Individual
import matplotlib.pyplot as plt
from constants import *
from typing import List

items = []

with open('./input2.csv', 'r') as archivo:
    lector_csv = csv.reader(archivo, delimiter=";")
    next(lector_csv)

    for fila in lector_csv:
        nombre = fila[0]
        valor = int(fila[1])
        peso = int(fila[2])

        item = Item(nombre, peso, valor)
        items.append(item)



def generate_initial_population(count=6) -> List[Individual]:
    population = []

    for _ in range(count):
        bits = [random.choice([0, 1]) for _ in items]
        individual = Individual(bits, items)
        population.append(individual)

    return population


def selection(population: List[Individual]) -> List[Individual]:
    random.shuffle(population)

    parents = []
    for i in range(0, len(population), 2):
        parent1 = population[i] if population[i].fitness() > population[i + 1].fitness() else population[i + 1]
        parent2 = population[i + 1] if population[i + 1].fitness() > population[i].fitness() else population[i]
        parents.extend([parent1, parent2])

    return parents


def crossover(parents: List[Individual]) -> List[Individual]:
    N = len(parents[0].bits)
    mid = N // 2

    child1 = parents[0].bits[:mid] + parents[1].bits[mid:]
    child2 = parents[1].bits[:mid] + parents[0].bits[mid:]

    return [Individual(child1, items), Individual(child2, items)]

def mutate(individuals: List[Individual]) -> List[Individual]:
    for individual in individuals:
        for i in range(len(individual.bits)):
            if random.random() < MUTATION_RATE:
                individual.bits[i] = ~individual.bits[i]


def next_generation(population: List[Individual]) -> List[Individual]:
    next_gen = []

    while len(next_gen) < len(population):
        parents = selection(population)

        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            children = crossover(parents)
            mutate(children)

        next_gen.extend(children)

    return next_gen[:len(population)]

def print_generation(population: List[Individual]):
    total_fitness = sum(individual.fitness() for individual in population)
    avg_fitness = total_fitness / len(population)

    for individual in population:
        print(individual.bits, individual.fitness())

    print()
    print("Average fitness:", avg_fitness)
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
    solutions = []
    for i in range(10):
        solution = solve_knapsack()
        print(solution)
        if solution.fitness() != 0:
            solutions.append(solution)
            print("Valor Total Mochila: " + str(solution.fitness()))
        print()