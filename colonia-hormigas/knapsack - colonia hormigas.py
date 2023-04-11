import csv
import time

items = []
capacidad_maxima = 64500

with open('./input5.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader) # Saltear la primera fila (etiquetas)

    # Leer los valores de la segunda y tercera columna de cada fila
    for row in csv_reader:
        name = row[0]
        value = int(row[1])
        weight = int(row[2])

        items.append((value, weight))       


# Implementar el algoritmo de colonia de hormigas
num_hormigas = 100
evaporacion = 0.5
alfa = 1
beta = 3
q = 100

mejor_solucion_valor = 0
mejor_solucion = []

# Inicializar feromonas en los items
feromonas = [1] * len(items)

# Inicializar variables de tiempo e iteraciones
tiempo_inicio = time.time()
iteracionGanadora = 0

for iteracion in range(100):
    # Inicializar las soluciones de las hormigas
    soluciones_hormigas = []
    for i in range(num_hormigas):
        solucion_hormiga = []
        peso_actual = 0
        valor_actual = 0
        while peso_actual < capacidad_maxima:
            probabilidades = []
            for j, item in enumerate(items):
                if j not in solucion_hormiga and peso_actual + item[1] <= capacidad_maxima:
                    # Calcular la probabilidad de añadir el item a la solución
                    probabilidad = feromonas[j] ** alfa * (item[0] / item[1]) ** beta
                    probabilidades.append((j, probabilidad))
            if not probabilidades:
                break
            # Seleccionar el item con la probabilidad más alta
            seleccionado = max(probabilidades, key=lambda x: x[1])
            solucion_hormiga.append(seleccionado[0])
            peso_actual += items[seleccionado[0]][1]
            valor_actual += items[seleccionado[0]][0]
        soluciones_hormigas.append((solucion_hormiga, valor_actual))

    # Actualizar feromonas en los items
    feromonas_nuevas = [0] * len(items)
    for solucion_hormiga, valor_hormiga in soluciones_hormigas:
        for item_index in solucion_hormiga:
            feromonas_nuevas[item_index] += q / valor_hormiga
    for i in range(len(feromonas)):
        feromonas[i] = (1 - evaporacion) * feromonas[i] + evaporacion * feromonas_nuevas[i]

    # Guardar la mejor solución encontrada
    mejor_solucion_actual = max(soluciones_hormigas, key=lambda x: x[1])
    if mejor_solucion_actual[1] > mejor_solucion_valor:
        mejor_solucion_valor = mejor_solucion_actual[1]
        mejor_solucion = mejor_solucion_actual[0]
        iteracionGanadora = i



tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio

print(f"Valor total mochila: {mejor_solucion_valor} \nIndice items: {mejor_solucion}")

peso_total = sum(items[i][1] for i in mejor_solucion)
print(f"Peso total mochila: {peso_total}")

print(f"Tiempo: {tiempo_total}")

print(f"Iteracion: {iteracionGanadora}")