import pickle
import random

with open('distance_matrix.data', 'rb') as f:
    distance_matrix = pickle.load(f)

city_array = []

alpla = 0.1
beta = 0.1
pheromon = 0.1

current_best = 0

current_city = 0


path_raw_value = lambda pheromon, distance, beta: pheromon * ((1/distance)**beta)


def reduction_to_one(element, array):
    return element / sum(array)


def get_raw_array()
    raw_array = []
    for i in distance_matrix[0]:
        raw_array.append(path_raw_value(pheromon, i, beta))
    return raw_array


after_reduction_array = []
for i in raw_array:
    after_reduction_array.append(reduction_to_one(i, raw_array))


def test():
    pass