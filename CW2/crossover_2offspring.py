from audioop import cross
from operator import index
import random
from re import X
from cv2 import split
from numpy import number
from random import choice, randrange

# constant parameter
pop_size = 400
demes = 20
number_of_sites = 50
mutation_rate = 1 / (2 * number_of_sites)
# 1 / (2 * number_of_sites)
# n_simulation = 30
ind_per_island = int(pop_size / demes)
# #################################

# initialization
pop = []
R_noise = []
fitness = []
new_pop = [[None for i in range(ind_per_island)] for j in range(demes)]
probability = []
mutated = []
max_prob_index = []
max_fitness = 0
generation = 0
# #################################


def Rij():
    #function to generate the different constant R for i,j
    R_noise = [[random.uniform(0.5, 1.0) for i in range(number_of_sites)]
               for j in range(number_of_sites)]
    return R_noise


def rand_key(number_of_sites):
    # function to generate individual with 2n binary
    length = 2 * number_of_sites
    individual = ""
    for i in range(length):
        temp = str(random.randint(0, 1))
        # temp = '1'
        individual += temp

    return (individual)


def pop_generator(pop_size):
    # function to generate 400 population of 2n binary
    for i in range(pop_size):
        random_str = rand_key(number_of_sites)
        pop.append(random_str)
        split_lists = [
            pop[x:x + ind_per_island]
            for x in range(0, len(pop), ind_per_island)
        ]
    return split_lists


def zip_fitness_eval(population, R_noise):
    maxi_fitness = 0
    fitness = []
    for i in range(demes):
        for j in range(ind_per_island):
            gene_i = population[i][j][:number_of_sites].count('1')
            gene_j = population[i][j][number_of_sites:].count('1')
            # for k in range(demes):
            #     for a in range(int(pop_size / demes)):
            #         for z in range(2 * number_of_sites):
            #             if pop[k][a][z] == '1' and z < number_of_sites:
            #                 i += 1
            #             if pop[k][a][z] == '1' and z >= number_of_sites:
            #                 j += 1

            fitness_equation = R_noise[gene_i - 1][gene_j - 1] * (2**gene_i +
                                                                  2**gene_j)
            fitness.append(fitness_equation)

    maxi_fitness = max(fitness)

    split_lists = [
        fitness[x:x + ind_per_island]
        for x in range(0, len(fitness), ind_per_island)
    ]
    return split_lists, maxi_fitness


def get_probability_list(deme_dict):
    fitness = deme_dict.values()
    total_fit = float(sum(fitness))
    relative_fitness = [f / total_fit for f in fitness]
    probabilities = [
        sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))
    ]
    return probabilities


def roulette_wheel_pop(population, probabilities, number):
    parents = []
    for n in range(number):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probabilities[i]:
                parents.append(individual)
                break
    return parents


def crossover(father, mother):
    child = []
    crossover_point = random.randint(0, (2*number_of_sites) - 1)
    for i in range(2 * number_of_sites):
        # if random.randint(0, 1) == 0:
        if i < crossover_point:

            child.append(father[0][i])
        else:
            child.append(mother[0][i])
        # else:
        #     if i < crossover_point:
        #         child.append(mother[0][i])
        #     else:
        #         child.append(father[0][i])
    xover = "".join(child)

    return xover


def mutation(chosen_one):
    child_list = []
    single_deme = []
    offsprings = []
    for i in range(demes):
        single_deme = []

        for j in range(ind_per_island):

            child_list = []
            if j == 0:
                child_list.append(chosen_one[i][j])
                child = "".join(child_list)
            else:
                for k in range(2 * number_of_sites):
                    if (random.random() < mutation_rate):
                        if chosen_one[i][j][k] == '1':
                            new_random_character = '0'

                        elif chosen_one[i][j][k] == '0':
                            new_random_character = '1'

                        child_list.append(new_random_character)
                        child = "".join(child_list)
                    else:
                        child_list.append(chosen_one[i][j][k])
                        child = "".join(child_list)

            single_deme.append(child)
        offsprings.append(single_deme)
    return offsprings


def max_fitness_index(fitness):
    max_index = []
    zzz = []
    for i in range(demes):
        max_value = max(fitness[i])
        zzz.append(max_value)
        max_index.append(fitness[i].index(max_value))

    # print(zzz)
    return max_index


# def replacement(pop, fitness_index, mutated):
#     #function to retain the highest fitness and also to replace one of the individual in the deme
#     for i in range(demes):
#         pop[i][choice([
#             i for i in range(0, ind_per_island) if i not in [fitness_index[i]]
#         ])] = mutated[i]
#     return pop


def migration(new_generation):

    # randomly selected individual and randomly selected deme
    for z in range(demes):
        # random_selected_individual_index = random.randint(0,ind_per_island-1)
        # random_selected_deme_index = random.randint(0, demes-1)
        # random_individual_location = random.randint(0, ind_per_island-1)
        # random_selected_deme_location = random.randint(0, demes - 1)

        random_selected_individual_index = random.randint(0, demes - 1)
        random_selected_deme_index = random.randint(0, demes - 1)
        random_individual_location = random.randint(1, demes - 1)
        new_generation[z][random_individual_location] = new_generation[
            random_selected_deme_index][random_selected_individual_index]
    # print(new_generation)
    return new_generation


R_noise = Rij()

total_population = pop_generator(pop_size)
# total_population = [['11111111111111111111' for i in range(ind_per_island)] for j in range(demes)]
zzz = R_noise[number_of_sites - 1][number_of_sites - 1] * (
    2**(number_of_sites) + 2**(number_of_sites))

while max_fitness != zzz:

    # print('fitness calculation landscape')
    fitness, max_fitness = zip_fitness_eval(total_population, R_noise)
    #print(len(fitness))``
    # print(max_fitness)

    #print("maximum fitness index")
    index_fit = max_fitness_index(fitness)
    #print(len(maximum_fitness_index))


    for i in range(demes):
        for j in range(ind_per_island):
            if j == 0:
                new_pop[i][j] = total_population[i][index_fit[i]]

            else:
                # deme_dict = dict(zip(total_population[i], fitness[i]))
                # parents = roulette_wheel_pop(
                #     total_population[i], get_probability_list(deme_dict), 2)
                # new_pop[i][j]= crossover(parents)
                deme_selected = random.randint(0, demes - 1)
                deme_dict = dict(zip(total_population[deme_selected], fitness[deme_selected]))
                father = roulette_wheel_pop(total_population[deme_selected],get_probability_list(deme_dict), 1)


                deme_selected = random.randint(0, demes - 1)
                deme_dict = dict(zip(total_population[deme_selected], fitness[deme_selected]))
                mother = roulette_wheel_pop(total_population[deme_selected],get_probability_list(deme_dict), 1)


                new_pop[i][j] = crossover(father, mother)

    #print("mutation")
    #mutated size is 20x20
    mutated = mutation(new_pop)
    # print(mutated[0][0])
    # print(mutated)

    #print('migrated')
    # new_migrated_generation = migration(mutated)
    #print(len(new_migrated_generation))

    generation += 1
    print(generation)

    total_population = mutated
    # total_population = new_pop
    mutated = []

    for i in range(demes):
        print(total_population[i][0])
    if max_fitness == R_noise[number_of_sites - 1][number_of_sites - 1] * (
            2**(number_of_sites) + 2**(number_of_sites)):
        print('hamkachan diuleilou mou waste of time')