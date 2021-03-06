# -*- coding: utf-8 -*-
from copy import deepcopy
from itertools import repeat
from pickle import load
from random import random
from time import time


# region functions
def get_raw_value_of_path(distance, pheromone, beta):
    """Calculates value of the specific path based on it's distance,
    pheromone, and beta values

    Return 0 to avoid zero division error and due to further usage of
    that function where. -1 is the representative of way that should not be
    attended, and 0 as a return of this function help to build proper execution
    of get_random_way_from_list function(0 is the way to ignore attended ways)

    :param distance: The distance value of the path
    :type distance: float
    :param pheromone: Value of the pheromone on that path
    :type pheromone: float
    :param beta: Coefficient of how much ants relies on pheromone value, gets passed to subfunction
    :type beta: float
    :return: Returns value calculated by formula if distance is bigger
    than zero, to avoid ZeroDivisionError. Otherwise returns zero.
    :rtype: float, 0
    """

    if distance > 0:
        return round(pheromone * ((1 / distance) ** beta), 4)
    else:
        return 0


def get_reducted_value_of_path(element_value, array):
    """Gets the path value relative to the sum of all elements of the list

    :param element_value: Value of the element from the list
    :type element_value: float, 0
    :param array: List containing all the values
    :type array: list
    :return: Returns reducted value of the element
    :rtype: float
    """

    return element_value / sum(array)


def summation_of_matrices(first_matrix, second_matrix):
    """Adding two double dimensional lists. Uses to update pheromone matrix and save survived ant path to
    increase chance of choosing the way of the ant that created second matrix

    :param first_matrix: base pheromone matrix that ants use
    :type first_matrix: list
    :param second_matrix: pheromone matrix that represents ant's path
    :type second_matrix: list
    :return: new global pheromone matrix that ants will be using
    :rtype: list
    """

    result_matrix = [[0 for _ in range(len(first_matrix))]
                     for _ in range(len(first_matrix))]

    for i in range(len(first_matrix)):
        for j in range(len(second_matrix)):
            result_matrix[i][j] = first_matrix[i][j] + second_matrix[i][j]

    return result_matrix


def subtraction_of_matrices(first_matrix, second_matrix):
    """Subtracting one matrix from another. Uses to update pheromone matrix and save died ant path to
    decrease chance of choosing the way of the ant that created second matrix

    :param first_matrix: base pheromone matrix that ants use
    :type first_matrix: list
    :param second_matrix: pheromone matrix that represents ant's path
    :type second_matrix: list
    :return: new global pheromone matrix that ants will be using
    :rtype: list
    """

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


def get_random_way_from_list(array):
    """Gets one way from the list of reducted values of the ways.

    Comparing the random value to the sum of the raw values, starting from first until
    the sum is not bigger than the random value from the random function. If sum of all
    the values is not bigger than random value(due to rounding it's possible to reduce all
    the values of the array to one, but still get the sum lower than one), than it will
    get another random value and will try to get sum bigger than new random value.
    Does this until sum of the values is not greater than random value.

    :param array: list of reducted values
    :type array: list
    :return: identifier of element that represents it's number in the list
    :rtype: int
    """

    while True:
        rand = round(random(), 4)
        summ = 0
        for element in range(len(array)):
            if summ + array[element] > rand:
                return element
            else:
                summ += array[element]


def choose_from_suitable_ways(temp_distance_matrix, pheromone_matrix, current_city, beta):
    # TODO:
    #     doc
    """

    :param temp_distance_matrix:
    :param pheromone_matrix:
    :param current_city:
    :param beta: Coefficient of how much ants relies on pheromone value
    :type beta: float
    :return:
    :rtype:
    """

    raw_values_array = \
        list(
            map(
                get_raw_value_of_path, temp_distance_matrix[current_city], pheromone_matrix[current_city], repeat(beta))
        )
    reducted_value_array = \
        [round(
            get_reducted_value_of_path(value, raw_values_array), 4) for value in raw_values_array]

    return get_random_way_from_list(reducted_value_array)


def one_try(distance_matrix, pheromone_matrix, amount_of_ants, beta):
    # TODO:
    #   doc
    #   add check for TabuList
    #   add blocking of all the ways that goes to a visited vertices
    """

    :param distance_matrix:
    :param pheromone_matrix:
    :param amount_of_ants:
    :param beta: Coefficient of how much ants relies on pheromone value, gets passed to subfunction
    :type beta: float
    :return:
    :rtype:
    """

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
        temp_pheromone_matrix = [[0 for _ in range(len(pheromone_matrix))]
                                 for _ in range(len(pheromone_matrix))]

        while True:
            # if not all cities are visited
            if not all(city == -1 for city in city_to_visit):

                # if not all ways are visited
                if not all(ways == -1 for ways in
                           temp_distance_matrix[current_city]):

                    # using method to choose the way out of all available
                    # paths from current point
                    chosen_way = choose_from_suitable_ways(
                        temp_distance_matrix,
                        pheromone_matrix,
                        current_city,
                        beta)

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
                    pheromone_matrix = subtraction_of_matrices(
                        pheromone_matrix, temp_pheromone_matrix)
                    break
            else:
                # increase value of alive ants and
                # update global variables to collect statistic
                ants_survived += 1
                total_distance += temp_total_distance
                pheromone_matrix = summation_of_matrices(
                    pheromone_matrix, temp_pheromone_matrix)
                if max_distance < temp_total_distance:
                    max_distance = temp_total_distance
                if min_distance > temp_total_distance > 0:
                    min_distance = temp_total_distance
                break
    print(min_distance)


def main():
    # TODO:
    #     doc
    #     apply threads:
    #         apply gradient descent
    with open('distance_matrix.data', 'rb') as file:
        o_distance_matrix = load(file)

    default_pheromone_value = 0.01
    pheromone_matrix = [[default_pheromone_value
                         for _ in range(len(o_distance_matrix))]
                        for _ in range(len(o_distance_matrix))]
    alpha = 0.1
    beta = 0.5
    one_try(o_distance_matrix, pheromone_matrix, 200, beta)


if __name__ == "__main__":
    start_time = time()
    main()
    # display execution time
    print(f'Total execution time: {round(time() - start_time, 3)}s\n\n')
