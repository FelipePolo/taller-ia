import csv
import time
import matplotlib.pyplot as plt

items = []
with open('./input2.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=";")
    next(csv_reader) # Saltear la primera fila (etiquetas)
    for row in csv_reader:
        items.append((int(row[1]), int(row[2])))

num_hormigas, capacidad_maxima, evaporacion, alfa, beta, q = 50, 7800, 0.2, 1, 2, 100
feromonas = [1] * len(items)
mejor_solucion, mejor_solucion_valor, iteracion_mejor_solucion = [], 0, 0
valores_convergencia = []

tiempo_inicio = time.time()
for iteracion in range(100):
    soluciones_hormigas = []
    for i in range(num_hormigas):
        solucion_hormiga, peso_actual, valor_actual = [], 0, 0
        while peso_actual < capacidad_maxima:
            probabilidades = [(j, feromonas[j] ** alfa * (valor / peso) ** beta) for j, (valor, peso) in enumerate(items) if j not in solucion_hormiga and peso_actual + peso <= capacidad_maxima]
            if not probabilidades:
                break
            seleccionado = max(probabilidades, key=lambda x: x[1])
            solucion_hormiga.append(seleccionado[0])
            peso_actual += items[seleccionado[0]][1]
            valor_actual += items[seleccionado[0]][0]
        soluciones_hormigas.append((solucion_hormiga, valor_actual))

    feromonas_nuevas = [0] * len(items)
    for solucion_hormiga, valor_hormiga in soluciones_hormigas:
        for item_index in solucion_hormiga:
            feromonas_nuevas[item_index] += q / valor_hormiga
    feromonas = [(1 - evaporacion) * f + evaporacion * f_nueva for f, f_nueva in zip(feromonas, feromonas_nuevas)]

    mejor_solucion_actual = max(soluciones_hormigas, key=lambda x: x[1])
    if mejor_solucion_actual[1] > mejor_solucion_valor:
        mejor_solucion_valor, mejor_solucion, iteracion_mejor_solucion = mejor_solucion_actual[1], mejor_solucion_actual[0], i
    valores_convergencia.append(mejor_solucion_valor)

tiempo_total = time.time() - tiempo_inicio

print(f"Valor total mochila: {mejor_solucion_valor}")
print(f"Indice items: {mejor_solucion}")
print(f"Peso total mochila: {sum(peso for valor, peso in [items[i] for i in mejor_solucion])}")
print(f"Tiempo: {tiempo_total}")
print(f"Índice de la iteración donde se encontró la mejor solución: {iteracion_mejor_solucion}")

plt.plot(valores_convergencia)
plt.xlabel('Iteración')
plt.ylabel('Mejor solución encontrada')
plt.title('Gráfica de convergencia')
plt.show()
