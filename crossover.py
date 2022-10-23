from itertools import count
from mimetypes import init
import string
import random

fitness_score = 0
answer = "Methinks it is like a weasel"
length = len(answer)
letters = string.ascii_letters + " "
parent = ''.join(random.choice(letters) for i in range(length))
population = []
population_count = 500
mutation_rate = 1
number_of_iterations = 0

def initialize_pop():
    for x in range(population_count):
        letters = string.ascii_letters + " "
        individual_population = ''.join(
            random.choice(letters) for i in range(length))
        population.append(individual_population)

    return population


population = initialize_pop()
print(population)


def fitness(string):
    fitness_score = 0
    for i in range(length):
        if string[i] == answer[i]:
            fitness_score += 1

    return fitness_score


def crossover(father, mother):
    for i in range(length):
        if (random.random() < 0.5):
            child.append(father[i])
        else:
            child.append(mother[i])
    xover = "".join(child)
    return xover


def mutation(string):
    for i in range(length):
        if (random.random() < (mutation_rate / length)):
            new_random_character = random.choice(letters)
            child_list.append(new_random_character)
            child = "".join(child_list)
        else:
            child_list.append(string[i])
            child = "".join(child_list)

    return child


while fitness_score != 28:
    child = []
    child_list = []

    father1 = population[random.randint(0, population_count-1)]
    mother1 = population[random.randint(0, population_count-1)]
    fit_fat = fitness(father1)
    fit_mot = fitness(mother1)

    if (fit_fat > fit_mot):
        parent1 = father1
    else:
        parent1 = mother1

    father2 = population[random.randint(0, population_count-1)]
    mother2 = population[random.randint(0, population_count-1)]
    fit_fat = fitness(father2)
    fit_mot = fitness(mother2)

    if (fit_fat > fit_mot):
        parent2 = father2
    else:
        parent2 = mother2

    crossover_children = crossover(parent1, parent2)
    mutated_children = mutation(crossover_children)
    fitness_score = fitness(mutated_children)
    print(mutated_children + " , " + str(fitness_score))

    rand_pop_A = random.randint(0, population_count-1)
    rand_pop_B = random.randint(0, population_count-1)
    pop_A = population[rand_pop_A]
    pop_B = population[rand_pop_B]

    fit_A = fitness(pop_A)
    fit_B = fitness(pop_B)
    if (fit_A > fit_B):
        population[rand_pop_B] = mutated_children
    else:
        population[rand_pop_A] = mutated_children

    number_of_iterations +=1

print("number of iterations: " + str(number_of_iterations))