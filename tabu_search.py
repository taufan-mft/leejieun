import requests
import numpy as np
import random

mockup_response = {
    'destination_addresses': ['585 Schenectady Ave, Brooklyn, NY 11203, USA', '102-01 66th Rd, Queens, NY 11375, USA'],
    'origin_addresses': ['P.O. Box 793, Brooklyn, NY 11207, USA'], 'rows': [{'elements': [
        {'distance': {'text': '3.4 mi', 'value': 5407}, 'duration': {'text': '19 mins', 'value': 1139}, 'status': 'OK'},
        {'distance': {'text': '8.5 mi', 'value': 13744}, 'duration': {'text': '24 mins', 'value': 1438},
         'status': 'OK'}]}], 'status': 'OK'}


class TabuSearch:
    def __init__(self, max_iteration, number_of_customer):
        self.max_iteration = max_iteration
        self.number_of_customer = number_of_customer
        self.api_key = 'AIzaSyDTA4A1s4ZYYNvzVdlHF3Lxpp4UAhRyz08'
        self.destinations = ['-7.391411,109.258934', '-7.393778,109.244960', '-7.401416,109.245107',
                             '-7.396291,109.265564', '-7.405146,109.245170']
        self.matrix = np.array([])

    def fetch_matrix(self, origin, destinations):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
        params = {
            'key': self.api_key,
            'origins': origin,
            'destinations': destinations,
        }
        resp = requests.get(url, params=params)
        received_array = resp.json()['rows'][0]['elements']
        temp = []
        for index, data in enumerate(received_array):
            temp.append(data['distance']['value'])
        return temp

    def build_matrix(self):
        number_of_destinations = len(self.destinations)
        parsed_destinations = '|'.join(map(str, self.destinations))
        matrix = np.zeros((number_of_destinations, number_of_destinations))
        for idx, destination in enumerate(self.destinations):
            result = self.fetch_matrix(destination, parsed_destinations)
            matrix[idx] = result
        print(matrix)
        return matrix

    @staticmethod
    def swap_move(arr):
        i1, i2 = random.sample(arr[1:len(arr) - 1], 2)
        arr[i1], arr[i2] = arr[i2], arr[i1]
        return {
            'moves': (arr[i1], arr[i2]),
            'arr': arr,
        }

    def calculate_distance(self, solution):
        distance = 0
        for idx, _ in enumerate(solution):
            if idx is not len(solution) - 1:
                print('distance from', solution[idx], solution[idx+1], self.matrix[solution[idx], solution[idx + 1]])
                distance += self.matrix[solution[idx], solution[idx + 1]]
        return distance

    def generate_initial_solution(self):
        self.matrix = self.build_matrix()
        result = [0]
        current = 0
        distance = 0
        total_distance = 0
        for _ in enumerate(self.destinations):
            if len(result) is len(self.destinations) - 1:
                break
            distance_matrix = self.matrix[current]
            min_value = min(i for i in distance_matrix if i > 0 and i != distance)
            at = np.where(distance_matrix == min_value)
            result_index = at[0][0]
            result.append(result_index)
            current = result_index
            distance = min_value
            total_distance += distance
        result.append(0)
        print(result)
        print('Total distance: ', self.calculate_distance(result))
        swapped = self.swap_move(result)
        print('swapped', swapped['moves'], 'result', swapped['arr'])
        new_distance = self.calculate_distance(swapped['arr'])
        print('new distance', new_distance)


tasya = TabuSearch(max_iteration=5, number_of_customer=2)
tasya.generate_initial_solution()
