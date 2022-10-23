from operator import index
import random
from cv2 import split
from numpy import number
from random import choice

# constant parameter
pop_size = 400
demes = 20
number_of_sites = 20
mutation_rate = 1 / (2 * number_of_sites)
n_simulation = 30
# #################################

# initialization
pop = []
R_noise = []
fitness = []
selected_offspring_each_deme = []
probability = []
mutated = []
max_prob_index = []
# #################################


def Rij():
    R_noise = [[random.uniform(0.5, 1.0) for i in range(number_of_sites)]
               for j in range(number_of_sites)]
    return R_noise


def rand_key(number_of_sites):
    # function to generate individual with 2n binary
    length = 2 * number_of_sites
    individual = ""
    for i in range(length):
        temp = str(random.randint(0, 1))
        individual += temp

    return (individual)


def pop_generator(pop_size):
    # function to generate 400 population of 2n binary
    for i in range(pop_size):
        random_str = rand_key(number_of_sites)
        pop.append(random_str)

    return pop


# def deme_subpopulation(pop):
#     # function to split 400 pop into 20 demes of size 20
#     pop = pop_generator(pop_size)
#     split_lists = [pop[x:x + demes] for x in range(0, len(pop), demes)]

#     return split_lists


def zip_fitness_eval(pop, R_noise):
    j = 0
    i = 0
    for a in range(len(pop)):
        for z in range(2 * number_of_sites):
            if pop[a][z] == '1' and z < number_of_sites:
                i += 1
            if pop[a][z] == '1' and z > number_of_sites:
                j += 1

        fitness_equation = R_noise[i][j] * (2**i + 2**j)
        fitness.append(fitness_equation)
        i = 0
        j = 0

    return fitness


def get_probability_list(deme_dict):
    fitness = deme_dict.values()
    total_fit = float(sum(fitness))
    relative_fitness = [f / total_fit for f in fitness]
    probabilities = [
        sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))
    ]
    # max_value = max(probabilities)
    # max_prob_index.append(probabilities.index(max_value))

    return probabilities


def roulette_wheel_pop(population, probabilities, number):
    chosen = []
    for n in range(number):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probabilities[i]:
                chosen.append(individual)
                break
    return chosen


def fitness_proportionate_selection(pop, fitness):
    for i in range(demes):
        deme_dict = dict(
            zip(pop[i * number_of_sites:(i + 1) * number_of_sites],
                fitness[i * number_of_sites:(i + 1) * number_of_sites]))
        selected_offspring_each_deme.append(
            roulette_wheel_pop(
                pop[i * number_of_sites:(i + 1) * number_of_sites],
                get_probability_list(deme_dict), 1))

    return selected_offspring_each_deme


def mutation(string):
    child_list = []
    for i in range(2 * number_of_sites):
        if (random.random() < (1 / 2 * number_of_sites)):
            new_random_character = random.choice(['0', '1'])
            child_list.append(new_random_character)
            child = "".join(child_list)
        else:
            child_list.append(string[i])
            child = "".join(child_list)

    return child


def max_fitness_index(total_fitness):
    max_index = []
    split_lists = [
        pop[x:x + demes] for x in range(0, len(total_fitness), demes)
    ]
    for i in range(demes):
        max_value = max(split_lists[i])
        max_index.append(split_lists[i].index(max_value))
    return max_index


def replacement(pop, fitness_index, mutated):
    pop_split_lists = [pop[x:x + demes] for x in range(0, len(pop), demes)]
    for i in range(demes):
        pop_split_lists[i][choice([
            i for i in range(0, number_of_sites)
            if i not in [fitness_index[i]]
        ])] = mutated[i]
    return pop_split_lists


total_population = pop_generator(pop_size)
print("pop")
print(total_population)
R_noise = Rij()
total_fitness = zip_fitness_eval(total_population, R_noise)
print("maximum fitness index")
fitness_index = max_fitness_index(total_fitness)
print(fitness_index)

print("fitness")
print(total_fitness)
yyy = fitness_proportionate_selection(total_population, total_fitness)
print("selection")
print(yyy)

for i in range(demes):
    mutated.append(mutation(yyy[i]))
print("mutation")
print(mutated)

print('replaced')
print(replacement(total_population, fitness_index, mutated))