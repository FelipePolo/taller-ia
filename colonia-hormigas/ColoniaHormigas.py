import csv
import time
import matplotlib.pyplot as plt


def read_data(filename):
    items = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader) # Saltear la primera fila (etiquetas)

        # Leer los valores de la segunda y tercera columna de cada fila
        for row in csv_reader:
            items.append((int(row[1]), int(row[2]))) 
    return items

def ant_colony_optimization(items, max_weight, num_ants=50, evaporation=0.5, alpha=1, beta=2, q=100, num_iterations=100):
    # Inicializar feromonas en los items
    pheromones = [1] * len(items)

    # Inicializar variables de tiempo y mejor solución
    start_time = time.time()
    best_solution = []
    best_value = 0

    for iteration in range(num_iterations):
        # Inicializar las soluciones de las hormigas
        solutions = []
        for i in range(num_ants):
            solution = []
            weight = 0
            value = 0
            while weight < max_weight:
                probabilities = [(j, pheromones[j] ** alpha * (item[0] / item[1]) ** beta) for j, item in enumerate(items) if j not in solution and weight + item[1] <= max_weight]
                if not probabilities:
                    break
                # Seleccionar el item con la probabilidad más alta
                selected_item = max(probabilities, key=lambda x: x[1])[0]
                solution.append(selected_item)
                weight += items[selected_item][1]
                value += items[selected_item][0]
            solutions.append((solution, value))

        # Actualizar feromonas en los items
        pheromones_new = [0] * len(items)
        for solution, value in solutions:
            for item_index in solution:
                pheromones_new[item_index] += q / value
        pheromones = [(1 - evaporation) * p + evaporation * p_new for p, p_new in zip(pheromones, pheromones_new)]

        # Guardar la mejor solución encontrada
        best_solution_current, best_value_current = max(solutions, key=lambda x: x[1])
        if best_value_current > best_value:
            best_solution = best_solution_current
            best_value = best_value_current
            iteration_winner = iteration

    # Calcular tiempo total y peso total de la mochila
    total_time = time.time() - start_time
    total_weight = sum(items[i][1] for i in best_solution)

    return best_value, best_solution, total_weight, total_time, iteration_winner

# Ejemplo de uso
filename = './input2.csv'
max_weight = 7800
items = read_data(filename)
best_value, best_solution, total_weight, total_time, iteration_winner = ant_colony_optimization(items, max_weight)

print(f"Valor total mochila: {best_value}")
print(f"Indice items: {best_solution}")
print(f"Peso total mochila: {total_weight}")
print(f"Tiempo: {total_time}")
print(f"Iteracion ganadora: {iteration_winner}")

# Gráfica de convergencia
plt.plot(best_solution)
plt.title("Convergencia - ACO")
plt.xlabel("Iteración")
plt.ylabel("Valor de la función de costo")
plt.show()
