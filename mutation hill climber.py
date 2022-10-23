from itertools import count
from mimetypes import init
import string
import random

fitness_score = 0
answer = "Methinks it is like a weasel"
length = len(answer)
letters = string.ascii_letters + " "
parent = ''.join(random.choice(letters) for i in range(length))

def fitness(string):
    fitness_score = 0
    for i in range(length):
        if string[i] == answer[i]:
            fitness_score += 1

    return fitness_score

def mutation(string):
    for i in range(length):
        if(random.random()<(1/length)):
            new_random_character = random.choice(letters)
            child_list.append(new_random_character)
            child = "".join(child_list)
        else:
            child_list.append(string[i])
            child = "".join(child_list)

    return child

while fitness_score !=28:
    child_list = []
    child = mutation(parent)
    fitness_score = fitness(mutation(parent))
    if fitness(child)>fitness(parent):
        parent = child
        print(child, " , ", str(fitness(child)))

# print(random_sentence + " , " + str(fitness_score))


# while fitness_score != 28:
#     for i in range(length):
#         if random_sentence[i] != answer[i]:
#             l = list(random_sentence)
#             l[i] = random.choice(letters)
#             random_sentence = "".join(l)

#             if random_sentence[i] == answer[i]:
#                 fitness_score += 1
                
#         print(random_sentence + " , " + str(fitness_score))  

#             l = list(random_sentence)
#             l[i] = random.choice(letters)
#             random_sentence = "".join(l)

#             if random_sentence[i] == answer[i]:
#                 fitness_score += 1
                
#         print(random_sentence + " , " + str(fitness_score))  