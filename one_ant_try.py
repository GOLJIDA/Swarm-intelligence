import pickle
import random

# region data
with open('distance_matrix.data', 'rb') as f:
    o_distance_matrix = pickle.load(f)

pheromon_matrix = [[0.05 for i in range(len(o_distance_matrix))]
                   for i in range(len(o_distance_matrix))]
alpla = 0.1
beta = 0.1


# endregion


# region functions

def raw_path_value(distance, pheromon):
    global beta
    if distance > 0:
        return round(pheromon * ((1 / distance) ** beta), 4)
    else:
        return 0


def reducted_value(distance, array_sum):
    return distance / array_sum


# result = pheromon * ((1/distance)**beta)
def sum_matrix(matrixo, matrixt):
    result = [[0 for i in range(len(matrixo))] for i in range(len(matrixo))]
    for i in range(len(matrixo)):
        for j in range(len(matrixt[0])):
            result[i][j] = matrixo[i][j] + matrixt[i][j]
    return result


def sub_matrix(matrixo, matrixt):
    result = [[0 for i in range(len(matrixo))] for i in range(len(matrixo))]
    for i in range(len(matrixo)):
        for j in range(len(matrixt[0])):
            temp = matrixo[i][j] - matrixt[i][j]
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
    const_d_matrix = d_matrix * 1
    min_distance = 10000000000
    max_distance = 0
    total_distance = 0
    survived = 0
    counter = 0
    for go in range(amount_of_ants):
        city_to_visit = d_matrix[0]
        print(f'Ant number {counter + 1} is on his way')
        # temp variables
        temp_total_distance = 0
        current_city = 0
        with open('distance_matrix.data', 'rb') as f:
            temp_d_matrix= pickle.load(f)
        temp_p_matrix = [[0.01 for i in range(len(p_matrix))]
                         for i in range(len(p_matrix))]
        # while there are dots
        while True:
            city_to_visit_check = 0
            # calculations to choose way
            raw_values_array = list(map(raw_path_value, temp_d_matrix[current_city], p_matrix[current_city]))
            raw_value_sum = sum(raw_values_array)
            reducted_value_array = [round(reducted_value(distance, raw_value_sum), 4)
                                    for distance in raw_values_array]
            chosen_way = choose_way(reducted_value_array)
            # recording the data
            temp_total_distance += const_d_matrix[current_city][chosen_way]
            temp_d_matrix[current_city][chosen_way] = -1
            city_to_visit[chosen_way] = -1
            temp_p_matrix[current_city][chosen_way] += 0.01
            # changing the city
            current_city = chosen_way
            if not (map(lambda x: True if (sum(array_of_distances) > 0 for array_of_distances in x) else False, temp_d_matrix)):
            total_distance += temp_total_distance
            p_matrix = sum_matrix(p_matrix, temp_p_matrix)
            if max_distance < temp_total_distance:
                max_distance = temp_total_distance
            if 0 < temp_total_distance < min_distance:
                min_distance = temp_total_distance
            p_matrix = sub_matrix(p_matrix, temp_p_matrix)
            survived += 1
            break



main(o_distance_matrix, pheromon_matrix, 5000)
