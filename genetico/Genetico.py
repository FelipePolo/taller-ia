import csv
import random
import matplotlib.pyplot as plt
import time

# Función de evaluación para calcular la aptitud de una solución candidata
def evaluar_solucion(solucion, capacidad_maxima, datos):
    peso_total = 0
    valor_total = 0
    for i in range(len(solucion)):
        if solucion[i] == 1:
            peso_total += datos[i][1]
            valor_total += datos[i][0]
    if peso_total > capacidad_maxima:
        return 0
    else:
        return valor_total
    
 # Función para calcular peso
def evaluar_peso_solucion(solucion, capacidad_maxima, datos):
    peso_total = 0
    for i in range(len(solucion)):
        if solucion[i] == 1:
            peso_total += datos[i][1]
    if peso_total > capacidad_maxima:
        return 0
    else:
        return peso_total

# Función de selección de torneo
def seleccion_torneo(poblacion, aptitudes, tam_torneo):
    seleccionados = []
    for i in range(len(poblacion)):
        torneo = random.sample(range(len(poblacion)), tam_torneo)
        seleccionado = torneo[0]
        for j in range(1, tam_torneo):
            if aptitudes[torneo[j]] > aptitudes[seleccionado]:
                seleccionado = torneo[j]
        seleccionados.append(poblacion[seleccionado])
    return seleccionados

# Función de cruce de un solo punto
def cruce_un_punto(padres):
    punto_cruce = random.randint(1, len(padres[0])-1)
    hijo1 = padres[0][:punto_cruce] + padres[1][punto_cruce:]
    hijo2 = padres[1][:punto_cruce] + padres[0][punto_cruce:]
    return [hijo1, hijo2]

# Función de mutación
def mutacion(solucion, tasa_mutacion):
    for i in range(len(solucion)):
        if random.random() < tasa_mutacion:
            if solucion[i] == 0:
                solucion[i] = 1
            else:
                solucion[i] = 0
    return solucion

# Función principal del algoritmo genético
def algoritmo_genetico(datos, capacidad_maxima, tam_poblacion, tasa_mutacion, tasa_cruce, tam_torneo, num_iteraciones):
    # Crear población inicial de soluciones aleatorias
    poblacion = []
    for i in range(tam_poblacion):
        solucion = [random.randint(0, 1) for j in range(len(datos))]
        poblacion.append(solucion)

    # Inicializar la lista de aptitudes de la población
    aptitudes = [evaluar_solucion(solucion, capacidad_maxima, datos) for solucion in poblacion]

    # Inicializar la lista para almacenar la mejor aptitud de cada iteración
    mejores_aptitudes = []

    # Repetir hasta que se alcance el número máximo de iteraciones o se encuentre una solución aceptable
    for i in range(num_iteraciones):
        # Seleccionar padres para la próxima generación utilizando el método de selección de torneo
        padres = seleccion_torneo(poblacion, aptitudes, tam_torneo)

        # Cruzar los padres seleccionados utilizando el operador de cruce de un solo punto
        hijos = []
        for j in range(0, tam_poblacion, 2):
            if random.random() < tasa_cruce:
                hijos.extend(cruce_un_punto([padres[j], padres[j+1]]))
            else:
                hijos.extend([padres[j], padres[j+1]])

        # Mutar algunas soluciones seleccionadas aleatoriamente en la población
        hijos = [mutacion(hijo, tasa_mutacion) for hijo in hijos]

        # Evaluar la aptitud de cada solución en la nueva población
        aptitudes_hijos = [evaluar_solucion(solucion, capacidad_maxima, datos) for solucion in hijos]

        # Reemplazar la población actual con la nueva población
        poblacion = hijos
        aptitudes = aptitudes_hijos

        # Almacenar la mejor aptitud de esta iteración
        mejores_aptitudes.append(max(aptitudes))

    # Seleccionar la mejor solución de la última población como la solución óptima
    mejor_solucion = poblacion[aptitudes.index(max(aptitudes))]
    valor_mejor_solucion = max(aptitudes)

    # Mostrar resultados
    print(f"Tiempo de ejecución: {time.time()-start_time} segundos")
    print(f"Número de iteraciones: {num_iteraciones}")
    print(f"Mejor solución: {mejor_solucion}")
    print(f"Valor de la mejor solución: {valor_mejor_solucion}")
    print(f"mejor peso de la solución: {evaluar_peso_solucion(mejor_solucion, capacidad_maxima, datos)}")

    # Graficar la convergencia
    plt.plot(mejores_aptitudes)
    plt.title("Convergencia del algoritmo genético")
    plt.xlabel("Número de iteración")
    plt.ylabel("Mejor aptitud")
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

# Programa principal
if __name__ == '__main__':
    # Función para leer los datos del archivo CSV
    
    #datos, capacidad_maxima = read_file('./input2.csv')
    datos = []
    with open('./input2.csv', 'r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv, delimiter=";")
        firstRow = True
        for fila in lector_csv:
            datos.append((int(fila['valor']), int(fila['peso'])))
            if (firstRow == True):
                capacidad_maxima = int(fila['capacidad_maxima'])
                firstRow = False

    # Configurar parámetros del algoritmo
    tam_poblacion = 50
    tasa_mutacion = 0.1
    tasa_cruce = 0.8
    tam_torneo = 5
    num_iteraciones = 100

    # Ejecutar el algoritmo genético
    start_time = time.time()
    algoritmo_genetico(datos, capacidad_maxima, tam_poblacion, tasa_mutacion, tasa_cruce, tam_torneo, num_iteraciones)

