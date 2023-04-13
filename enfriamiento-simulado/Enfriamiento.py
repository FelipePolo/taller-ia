import csv
import random
from Annealer import Annealer
import matplotlib.pyplot as plt
import time


class KnapsackProblem(Annealer):
    def __init__(self, state, max_weight, items):
        self.max_weight = max_weight
        self.items = items
        super(KnapsackProblem, self).__init__(state)

    def move(self):
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        total_value = sum([self.items[i][0] for i in range(len(self.state)) if self.state[i] == 1])
        total_weight = sum([self.items[i][1] for i in range(len(self.state)) if self.state[i] == 1])
        if total_weight > self.max_weight:
            return -total_value
        else:
            return total_value

def run_simulated_annealing(max_weight, items):
    start_time = time.time()
    
    initial_state = [random.randint(0, 1) for _ in range(len(items))]
    problem = KnapsackProblem(initial_state, max_weight, items)
    state, energy = problem.anneal()

    convergencia = [elemento for elemento in problem.history if type(elemento) != list]

    end_time = time.time()

    print(f"Simulated Annealing -- Tiempo: {round(end_time - start_time, 5)} s")
    print(f"Iteraciones: {problem.steps}")
    print(f"Mejor solución encontrada: {state}")
    print(f"Valor total de la solución: {(-1)*energy}")

    # Gráfica de convergencia
    plt.plot(convergencia)
    plt.title("Convergencia - Enfriamiento Simulado")
    plt.xlabel("Iteración")
    plt.ylabel("Valor de la función de costo")
    plt.show()

def read_file(file_name):
    items = []
    max_weight = int; comp = False;
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader, None)
        for row in reader:
            if(comp == False):
                max_weight = int(row[0]);
                items.append([int(row[1]), int(row[2])])
                comp = True;
            else:
                items.append([int(row[1]), int(row[2])])
    return max_weight, items

if __name__ == '__main__':
    file_name = "./input2.csv"
    max_weight, items = read_file(file_name)
    run_simulated_annealing(max_weight, items)
