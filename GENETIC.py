import random
import numpy as np


def create_population(pop_n):
    """pop_n = size of population, number of generated soilmaps 20x20"""
    population = []
    for _ in range(pop_n):
        soilmap = np.zeros((20,20))
        for y in range(20):
            for x in range(20):
                soilmap[y][x] = random.randint(0, 3)
        population.append(soilmap)
    return population
    

def fitness(arr):
    """Scores single soilmap, soilmap with same soil tiles clustered as neighbors is scored higher"""
    fitscore=0
    for y in range(len(arr)):
        for x in range(len(arr)):
            if y>0:
                if arr[y][x]==arr[y-1][x]: #gorny sasiad
                    fitscore+=1
            if y<len(arr)-1:        
                if arr[y][x]==arr[y+1][x]: #dolny sasiad
                    fitscore+=1
            if x>0:
                if arr[y][x]==arr[y][x-1]: #lewy sasiad
                    fitscore+=1
            if x<len(arr)-1:
                if arr[y][x]==arr[y-1][x+1]: #prawy sasiad
                    fitscore+=1
    return fitscore

def evaluate_population(population, fitness_func):
    """Scores whole population of soilmaps, returns list of tuples (score, soilmap)"""
    evaled_population = []
    for s in population:
        evaled_population.append((fitness_func(s), s))
    return evaled_population

def select_parents(evaled_population):
    """Selects best performing half of soilmaps"""
    selected_parents = []
    halflen = int(len(evaled_population)/2)
    for i in range(halflen): #bierzemy tylko najlepsze soilmapy, bez fitscore
        selected_parents.append(evaled_population[i][1])
    return selected_parents

def crossover(p1, p2):
    """Crosses over two parents and creates two childrens"""
    c1, c2 = p1, p2
    c3, c4 = p1, p2
    if random.random() < 0.98: #2% szansy na brak krzyzowki, wtedy skopiowanie rodzicow 1:1
        hlenp1, hlenp2 = int(len(p1)/2), int(len(p2)/2) #half lenght p1, half lenght p2
        c1 = np.concatenate((p1[:hlenp1], p2[hlenp2:]))
        c2 = np.concatenate((p2[:hlenp2], p1[hlenp1:]))    
    return c1, c2 

def mutate(c):
    """Mutates children, 1%*3/4 chance per tile, 400 tiles, so avg 3 tiles changed"""
    for i in range(len(c)):
        for j in range(len(c[i])):
            if random.random() > 0.99: #1% szansy dla kazdego pola na kracie ze zmutuje typ gleby na inny (1% * 3/4)
                c[i][j] = random.choice([0, 1, 2, 3])
    return c


def create_children(parents):
    children = []
    for i in range(0, len(parents)-1):
        c1, c2 = crossover(parents[i], parents[i+1])
        c1 = mutate(c1)
        c2 = mutate(c2)
        children.append(c1)
        children.append(c2)
    return children

def genetic_mapmaker():
    pop_n = 300 #population size of soilmaps

    population = create_population(pop_n)

    for gen in range(30):
        evaled_population = evaluate_population(population, fitness)
        evaled_population.sort(key=lambda element: element[0], reverse= True)
        selected_parents = select_parents(evaled_population)
        children = create_children(selected_parents)
        population = children
        print(f"Gen {gen} fitscore: ",evaled_population[0][0])

    print(evaled_population[0][1])

    return evaled_population[0][1]

