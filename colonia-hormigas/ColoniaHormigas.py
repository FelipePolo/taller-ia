import csv
import random
import matplotlib.pyplot as plt
import time

# Leer los datos de entrada del archivo CSV
def read_csv_file(file_name):
    objects = []
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader) # omitir la primera fila (encabezados)
        for row in csv_reader:
            capacity = int(row[0])
            value = int(row[1])
            weight = int(row[2])
            objects.append((capacity, value, weight))
    return objects

# Inicializar los parámetros del algoritmo
def init_params(objects):
    pheromone = 0.1
    evaporation = 0.5
    ants = 10
    iterations = 100
    q = 10
    max_weight = sum([obj[2] for obj in objects])
    return pheromone, evaporation, ants, iterations, q, max_weight

# Inicializar la matriz de feromonas
def init_pheromone_matrix(objects):
    n = len(objects)
    pheromone_matrix = [[pheromone for j in range(n)] for i in range(n)]
    return pheromone_matrix

# Inicializar la matriz de visibilidad
def init_visibility_matrix(objects, max_weight):
    n = len(objects)
    visibility_matrix = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if objects[j][2] <= max_weight:
                visibility_matrix[i][j] = objects[j][1] / objects[j][2]
    return visibility_matrix

# Calcular la probabilidad de transición
def transition_probabilities(current_object, objects, pheromone_matrix, visibility_matrix, visited, q):
    n = len(objects)
    probabilities = [0 for i in range(n)]
    total_prob = 0
    for j in range(n):
        if j not in visited:
            numerator = (pheromone_matrix[current_object][j] ** q) * (visibility_matrix[current_object][j] ** q)
            denominator = sum([(pheromone_matrix[current_object][k] ** q) * (visibility_matrix[current_object][k] ** q) for k in range(n) if k not in visited])
            probabilities[j] = numerator / denominator
            total_prob += probabilities[j]
    if total_prob == 0:
        return [1/n for i in range(n)]
    return [p/total_prob for p in probabilities]

# Construir una solución utilizando la regla de transición estocástica
def build_solution(objects, pheromone_matrix, visibility_matrix, q):
    n = len(objects)
    max_weight = sum([obj[2] for obj in objects])
    visited = []
    weight = 0
    while weight < max_weight and len(visited) < n:
        current_object = visited[-1] if len(visited) > 0 else random.randint(0, n-1)
        probabilities = transition_probabilities(current_object, objects, pheromone_matrix, visibility_matrix, visited, q)
        next_object = random.choices(range(n), weights=probabilities)[0]
        visited.append(next_object)
        weight += objects[next_object][2]
    return visited

# Calcular el valor total de una solución
def calculate_value(solution, objects):
    value = 0
    weight = 0
    for i in solution:
        if weight + objects[i][2] <= objects[0][0]:
            value += objects[i][1]
            weight += objects[i][2]
        else:
            break
    return value

# Actualizar la matriz de feromonas con la solución construida
def update_pheromone_matrix(pheromone_matrix, solutions, objects, evaporation):
    n = len(objects)
    for i in range(n):
        for j in range(n):
            pheromone_matrix[i][j] *= (1 - evaporation)
    for solution in solutions:
        value = calculate_value(solution, objects)
        weight = sum([objects[i][2] for i in solution])
        for i in range(len(solution)-1):
            pheromone_matrix[solution[i]][solution[i+1]] += (1.0/value)

# Ejecutar una iteración del algoritmo
def run_iteration(objects, pheromone_matrix, visibility_matrix, ants, q):
    solutions = [build_solution(objects, pheromone_matrix, visibility_matrix, q) for i in range(ants)]
    best_solution = max(solutions, key=lambda x: calculate_value(x, objects))
    return best_solution, solutions

# Ejecutar el algoritmo de colonia de hormigas para resolver el problema de la mochila
def ant_colony_optimization(objects, pheromone, evaporation, ants, iterations, q, max_weight):
    pheromone_matrix = init_pheromone_matrix(objects)
    visibility_matrix = init_visibility_matrix(objects, max_weight)
    best_solution = None
    best_value = -1
    convergence_curve = []
    start_time = time.time()
    for i in range(iterations):
        print(f"Iteration {i+1} of {iterations}")
        best_solution, solutions = run_iteration(objects, pheromone_matrix, visibility_matrix, ants, q)
        update_pheromone_matrix(pheromone_matrix, solutions, objects, evaporation)
        best_value = calculate_value(best_solution, objects)
        convergence_curve.append(best_value)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nBest solution: {best_solution}")
    print(f"Best value: {best_value}")
    print(f"Elapsed time: {elapsed_time} seconds")
    print(f"Number of iterations: {iterations}")
    plt.plot(convergence_curve)
    plt.xlabel('Iterations')
    plt.ylabel('Best value')
    plt.show()

# Ejemplo de uso
if __name__ == '__main__':
    objects = read_csv_file('C:/Users/E1Ganso/Downloads/taller-ia-master/colonia-hormigas/input2.csv')
    pheromone, evaporation, ants, iterations, q, max_weight = init_params(objects)
    ant_colony_optimization(objects, pheromone, evaporation, ants, iterations, q, max_weight)
