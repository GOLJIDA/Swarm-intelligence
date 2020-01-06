# -*- coding: utf-8 -*-
from pickle import load
from random import random
from time import time
from copy import deepcopy


# region functions
def get_raw_value_of_path(distance, pheromone, beta):
    '''Calculates value of the specific path based on it's distance,
    pheromone, and beta values

    :param distance: The distance value of the path
    :type distance: float
    :param pheromone: Value of the pheromone on that path
    :type pheromone: float
    :param beta: Coefficient of how mych ants relies on pheromone value
    :type beta: float
    :return: Returns value calculated by formula if distance is bigger
    than zero, to avoid ZeroDivisionError. Otherwise returns zero
    :rtype: float, 0
    '''
    if distance > 0:
        return round(pheromone * ((1 / distance) ** beta), 4)
    else:
        return 0


def get_reducted_value_of_path(element_value, list):
    '''Gets the path value relative to the sum of all elements of the list

    :param element_value: Value of the element from the list
    :type element_value: float, 0
    :param list: List containing all the values
    :type list: list
    :return: Returns reducted value of the element
    :rtype: float
    '''
    return element_value / sum(list)


def sum_matrix(first_matrix, second_matrix):
    result_matrix = [[0 for _ in range(len(first_matrix))]
                     for _ in range(len(first_matrix))]
    for i in range(len(first_matrix)):
        for j in range(len(second_matrix)):
            result_matrix[i][j] = first_matrix[i][j] + second_matrix[i][j]
    return result_matrix


def sub_matrix(first_matrix, second_matrix):
    result_matrix = [[0 for _ in range(len(first_matrix))]
                     for _ in range(len(first_matrix))]
    for first_element in range(len(first_matrix)):
        for second_element in range(len(first_matrix)):
            temp = round(first_matrix[first_element][second_element] -
                         second_matrix[first_element][second_element], 2)
            if temp < 0.01:
                result_matrix[first_element][second_element] = 0.01
            else:
                result_matrix[first_element][second_element] = temp
    return result_matrix


def choose_way_random(array):
    rand = round(random(), 4)
    summ = 0
    for element in range(len(array)):
        if summ + array[element] > rand:
            return element
        else:
            summ += array[element]
    return len(array) - 1


def choose_way(temp_distance_matrix, pheromone_matrix, current_city):
    raw_values_array = list(map(
        get_raw_value_of_path, temp_distance_matrix[current_city],
        pheromone_matrix[current_city]))
    reducted_value_array =\
        [round(get_reducted_value_of_path(value, raw_values_array), 4)
         for value in raw_values_array]
    return choose_way_random(reducted_value_array)


def one_try(distance_matrix, pheromone_matrix, amount_of_ants):
    # set variables for ability to compare later
    max_distance = 0
    total_distance = 0
    min_distance = 10000000
    ants_survived = 0

    # for amount of ants
    for _ in range(amount_of_ants):
        temp_total_distance = 0
        current_city = 0
        city_to_visit = deepcopy(distance_matrix[0])
        temp_distance_matrix = deepcopy(distance_matrix)
        temp_pheromone_matrix = [[0 for i in range(len(pheromone_matrix))]
                                 for i in range(len(pheromone_matrix))]

        while True:

            # if not all cities are visited
            if not all(city == -1 for city in city_to_visit):

                # if not all ways are visited
                if not all(ways == -1 for ways in
                           temp_distance_matrix[current_city]):

                    # using method to choose the way out of all available
                    # pathes from current point
                    chosen_way = choose_way(
                        temp_distance_matrix,
                        pheromone_matrix,
                        current_city)

                    # updating temporal variables
                    # to track current state
                    temp_total_distance += \
                        temp_distance_matrix[current_city][chosen_way]

                    temp_distance_matrix[current_city][chosen_way] = -1
                    city_to_visit[current_city] = -1

                    temp_pheromone_matrix[current_city][chosen_way] += 0.01

                    # changing the city
                    current_city = chosen_way
                else:
                    # decrease value of pheromones on path because
                    # it leads to death
                    pheromone_matrix = sub_matrix(
                        pheromone_matrix, temp_pheromone_matrix)
                    break
            else:
                # increase value of alive ants and
                # update global variables to collect statistic
                ants_survived += 1
                total_distance += temp_total_distance
                pheromone_matrix = sum_matrix(
                    pheromone_matrix, temp_pheromone_matrix)
                if max_distance < temp_total_distance:
                    max_distance = temp_total_distance
                if min_distance > temp_total_distance > 0:
                    min_distance = temp_total_distance
                break


def main():
    with open('distance_matrix.data', 'rb') as file:
        o_distance_matrix = load(file)

    default_pheromone_value = 0.01
    pheromone_matrix = [[default_pheromone_value
                        for _ in range(len(o_distance_matrix))]
                        for _ in range(len(o_distance_matrix))]
    alpha = 0.1
    beta = 0.5


if __name__ == "__main__":
    start_time = time()
    main()
    # display excecution time
    print(f'Total excecution time: {round(time() - start_time, 3)}s\n\n')
