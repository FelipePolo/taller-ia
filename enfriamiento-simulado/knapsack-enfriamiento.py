import csv
import datetime
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


MAX_KNAPSACK_WEIGHT = 64500
INITIAL_TEMPERATURE = 100
COOLING_FACTOR = 0.99


items = []

# Abrir el archivo CSV y leer los valores
with open('./input5.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader) # Saltear la primera fila (etiquetas)

    # Leer los valores de la segunda y tercera columna de cada fila
    for row in csv_reader:
        name = row[0]
        value = int(row[1])
        weight = int(row[2])

        # Crear el objeto Item y agregarlo a la lista de items
        item = Item(name, weight, value)
        items.append(item)


def generate_initial_solution() -> Individual:
    bits = [
        random.choice([0, 1])
        for _ in items
    ]
    return Individual(bits)


def neighbor(solution: Individual) -> Individual:
    new_bits = solution.bits.copy()
    index = random.randrange(len(items))
    new_bits[index] = 1 - new_bits[index]
    return Individual(new_bits)


def acceptance_probability(old_fitness: float, new_fitness: float, temperature: float) -> float:
    if new_fitness > old_fitness:
        return 1.0
    else:
        return pow(2.71828, (new_fitness - old_fitness) / temperature)


def solve_knapsack() -> Individual:

    start_time = time.time()
    iteration_count = 0
    
    current_solution = generate_initial_solution()
    best_solution = current_solution

    temperature = INITIAL_TEMPERATURE
    while temperature > 1:
        iteration_count += 1
        for _ in range(1000):
            new_solution = neighbor(current_solution)
            old_fitness = current_solution.fitness()
            new_fitness = new_solution.fitness()
            ap = acceptance_probability(old_fitness, new_fitness, temperature)
            if ap > random.random():
                current_solution = new_solution
                if current_solution.fitness() > best_solution.fitness():
                    best_solution = current_solution
        temperature *= COOLING_FACTOR

    end_time = time.time()
    total_time = end_time - start_time
    print("Tiempo total empleado: " + str(datetime.timedelta(seconds=total_time)))
    print("Numero de iteraciones: " + str(iteration_count))

    return best_solution


if __name__ == '__main__':
    for i in range(5):
        solution = solve_knapsack()
        print(solution)
        if solution.fitness() == 0:
            print("Solucion no apta - sobrepasa el peso permitido")
        else:
            print("Valor Total Mochila:"+str(solution.fitness()))   
    
        print()
