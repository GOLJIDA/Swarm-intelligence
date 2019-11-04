import pickle
import random
import time
import copy


# region data
with open('distance_matrix.data', 'rb') as f:
    o_distance_matrix = pickle.load(f)

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


def reducted_value(value, array_sum):
    return value / array_sum



def sum_matrix(matrixo, matrixt):
    result = [[0 for i in range(len(matrixo))] for i in range(len(matrixo))]
    for i in range(len(matrixo)):
        for j in range(len(matrixt)):
            result[i][j] = matrixo[i][j] + matrixt[i][j]
    return result


def sub_matrix(matrixo, matrixt):
    result = [[0 for i in range(len(matrixo))] for i in range(len(matrixo))]
    for i in range(len(matrixo)):
        for j in range(len(matrixo)):
            temp = round(matrixo[i][j] - matrixt[i][j], 2)
            if temp < 0.01:
                result[i][j] = 0.01
            else:
                result[i][j] = temp
    return result


def choose_way(array):
    rand = round(random.random(), 4)
    summ = 0
    for i in range(len(array)):
        if summ + array[i] > rand:
            return i
        else:
            summ += array[i]
    return len(array) - 1
# endregion


def main(d_matrix, p_matrix, amount_of_ants):
    # function variables
    min_distance = 10000000000
    max_distance = 0
    total_distance = 0
    survived = 0
    counter = 0
    # go for amount of ants
    for _ in range(amount_of_ants):
        # print(f'Ant number {counter + 1} is on his way')        
        city_to_visit = copy.deepcopy(d_matrix[0])
        # temp variables
        temp_total_distance = 0
        current_city = 0
        temp_d_matrix = copy.deepcopy(d_matrix)
        temp_p_matrix = [[0 for i in range(len(p_matrix))]
                         for i in range(len(p_matrix))]
        # while there are dots
        # print(d_matrix)
        # print(p_matrix)
        while True:
            if not all(city == -1 for city in city_to_visit):
                if not all(ways == -1 for ways in temp_d_matrix[current_city]):
                    # calculations to choose way
                    raw_values_array = list(map(raw_path_value, temp_d_matrix[current_city], p_matrix[current_city]))
                    raw_value_sum = sum(raw_values_array)
                    reducted_value_array = [round(reducted_value(value, raw_value_sum), 4)
                                            for value in raw_values_array]
                    chosen_way = choose_way(reducted_value_array)

                    # recording the data
                    temp_total_distance += temp_d_matrix[current_city][chosen_way]
                    temp_d_matrix[current_city][chosen_way] = -1
                    city_to_visit[current_city] = -1
                    temp_p_matrix[current_city][chosen_way] += 0.01

                    # changing the city
                    current_city = chosen_way
                else:
                    p_matrix = sub_matrix(p_matrix, temp_p_matrix)
                    break
            else:
                survived += 1
                total_distance += temp_total_distance
                p_matrix = sum_matrix(p_matrix, temp_p_matrix)
                if max_distance < temp_total_distance:
                    max_distance = temp_total_distance
                if min_distance > temp_total_distance > 0:
                    min_distance = temp_total_distance
                break
        counter += 1
    print(total_distance)
    print(total_distance / counter)
    print(survived)
    print(max_distance)
    print(min_distance)


start_time = time.time()
main(o_distance_matrix, pheromon_matrix, 1000)
print(time.time() - start_time)
