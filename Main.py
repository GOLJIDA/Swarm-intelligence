import pickle
import random
import time
import copy

# region data
with open('distance_matrix.data', 'rb') as f:
    o_distance_matrix = pickle.load(f)

global pheromon_matrix
pheromon_matrix = [[0.01 for i in range(len(o_distance_matrix))]
                   for i in range(len(o_distance_matrix))]
alpha = 0.1
beta = 0.5
# endregion


# region functions
def raw_path_value(distance, pheromon):
    global beta
    if distance > 0:
        return round(pheromon * ((1 / distance) ** beta), 4)
    else:
        return 0


def reducted_value(value, array):
    return value / sum(array)


def sum_matrix(first_matrix, second_matrix):
    result_matrix = [[0 for i in range(len(first_matrix))]
                     for i in range(len(first_matrix))]
    for i in range(len(first_matrix)):
        for j in range(len(second_matrix)):
            result_matrix[i][j] = first_matrix[i][j] + second_matrix[i][j]
    return result_matrix


def sub_matrix(first_matrix, second_matrix):
    result_matrix = [[0 for i in range(len(first_matrix))]
                     for i in range(len(first_matrix))]
    for i in range(len(first_matrix)):
        for j in range(len(first_matrix)):
            temp = round(first_matrix[i][j] - second_matrix[i][j], 2)
            if temp < 0.01:
                result_matrix[i][j] = 0.01
            else:
                result_matrix[i][j] = temp
    return result_matrix


def choose_way_random(array):
    rand = round(random.random(), 4)
    summ = 0
    for i in range(len(array)):
        if summ + array[i] > rand:
            return i
        else:
            summ += array[i]
    return len(array) - 1


def choose_way(temp_distance_matrix, pheromon_matrix, current_city):
    raw_values_array = list(map(
        raw_path_value, temp_distance_matrix[current_city],
        pheromon_matrix[current_city]))
    reducted_value_array = [round(reducted_value(value, raw_values_array), 4)
                            for value in raw_values_array]
    chose = choose_way_random(reducted_value_array)
    return chose


def update_global_sum_values(temp_total_distance, temp_pheromon_matrix):
    global min_distance
    global max_distance
    global total_distance
    global pheromon_matrix

    total_distance += temp_total_distance
    pheromon_matrix = sum_matrix(
        pheromon_matrix, temp_pheromon_matrix)
    if max_distance < temp_total_distance:
        max_distance = temp_total_distance
    if min_distance > temp_total_distance > 0:
        min_distance = temp_total_distance


def update_temp_variables(current_city, chosen_way):
    global temp_distance_matrix
    global temp_pheromon_distance
    global temp_total_distance
    global city_to_visit

    temp_total_distance += \
        temp_distance_matrix[current_city][chosen_way]
    temp_distance_matrix[current_city][chosen_way] = -1
    city_to_visit[current_city] = -1
    temp_pheromon_matrix[current_city][chosen_way] += 0.01
# endregion


def main(distance_matrix, pheromon_matrix, amount_of_ants):
    # global variables to count stuff
    global min_distance
    global max_distance
    global total_distance
    global ants_survived
    # global temporal variables to track state of ant
    global city_to_visit
    global temp_total_distance
    global temp_pheromon_matrix
    global temp_distance_matrix

    # set variables for ability to compare later
    max_distance = 0
    total_distance = 0
    min_distance = 10000000
    ants_survived = 0

    # for amount of ants
    for _ in range(amount_of_ants):
        temp_total_distance = 0
        current_city = 0
        city_to_visit = copy.deepcopy(distance_matrix[0])
        temp_distance_matrix = copy.deepcopy(distance_matrix)
        temp_pheromon_matrix = [[0 for i in range(len(pheromon_matrix))]
                                for i in range(len(pheromon_matrix))]

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
                        pheromon_matrix,
                        current_city)

                    # updating temporal variables
                    # to track current state
                    update_temp_variables(current_city, chosen_way)

                    # changing the city
                    current_city = chosen_way
                else:
                    # decrease value of pheromons on path because
                    # it leads to death
                    pheromon_matrix = sub_matrix(
                        pheromon_matrix, temp_pheromon_matrix)
                    break
            else:
                # increase value of alive ants and
                # update global variables to collect statistic
                ants_survived += 1
                update_global_sum_values(
                    temp_total_distance,
                    temp_pheromon_matrix)
                break

    print(f'\n\nTotal distance covered: {total_distance}km \n'
          f'Average distance: {total_distance / ants_survived}km \n'
          f'Ants survived: {ants_survived} \n'
          f'Longest way: {max_distance}km \n'
          f'Shortest way: {min_distance}km')


start_time = time.time()
main(o_distance_matrix, pheromon_matrix, 100)
print(f'Total excecution time: {round(time.time() - start_time, 3)}s\n\n')
