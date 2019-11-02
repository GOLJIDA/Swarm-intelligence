from settings import API_KEY
import requests
import pickle
import time


distance_matrix = []
city_array = []
counter = 0


with open('cities.txt', 'r') as file:
    for line in file:
        city_array.append(line.replace('\n', ''))


def get_place_id(place_str):
    while True:
        try:
            result = requests.get('https://maps.googleapis.com/maps/api/'
            + 'place/findplacefromtext/json?key='
            + API_KEY + '&input=' + place_str + '&inputtype=textquery').json()
            return(result.get('candidates')[0].get('place_id'))
        except:
            print(result)
            time.sleep(60)
            

def get_distance_between_cities(first_city, second_city):
    fc_place_id = get_place_id(first_city)
    sc_place_id = get_place_id(second_city)
    origin = fc_place_id
    destination = sc_place_id

    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=place_id:'
    + origin + '&destinations=place_id:' + destination + '&key=' + API_KEY).json()

    km = r.get('rows')[0].get('elements')[0].get('distance').get('value')
    distance = km // 1000
    return distance


for i in city_array:
    distance_matrix.append([])
    for j in city_array:
        start_time = time.time()
        dist = get_distance_between_cities(i, j)
        execution_time = time.time() - start_time
        if i == j:
            dist = -1
        counter += 1
        print('Distance between ' + i + ' and ' + j + ' is ' + str(dist) + 'km')
        print(str(counter/25) + '% done')
        print(f'Request took {round(execution_time, 2)} seconds\n')
        distance_matrix[-1].append(dist)
        time.sleep(5)


with open('distance_matrix.data', 'wb') as f:
    pickle.dump(distance_matrix, f)
