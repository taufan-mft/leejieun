from copy import copy

import requests
import numpy as np
import random


class TabuSearch:
    def __init__(self, max_iteration, number_of_customer):
        self.max_iteration = max_iteration
        self.number_of_customer = number_of_customer
        self.tabu_list = []
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
        copied = copy(arr)
        i1, i2 = random.sample(copied[1:len(copied) - 1], 2)
        idx = arr.index(i1)
        idx2 = arr.index(i2)
        copied[idx], copied[idx2] = copied[idx2], copied[idx]
        return {
            'moves': (copied[idx], copied[idx2]),
            'arr': copied,
        }

    def calculate_distance(self, solution):
        distance = 0
        for idx, _ in enumerate(solution):
            if idx is not len(solution) - 1:
                distance += self.matrix[solution[idx], solution[idx + 1]]
        return distance

    def generate_neighbourhood(self, initial_solution):
        temp = []
        for i in range(5):
            swapped_arr = self.swap_move(initial_solution)
            temp.append({
                **swapped_arr,
                'distance': self.calculate_distance(swapped_arr['arr'])
            })
        return temp

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
        print('Initial Solution')
        print(result)
        print('Total distance: ', self.calculate_distance(result))
        return result

    def haleluya(self):
        initial_solution = self.generate_initial_solution()
        iteration = 0
        neighbourhood = self.generate_neighbourhood(initial_solution)
        distance = self.calculate_distance(initial_solution)
        print('the neighbour', neighbourhood)


tasya = TabuSearch(max_iteration=100, number_of_customer=2)
tasya.haleluya()
