import os
from copy import copy
import time
import math
import requests
import numpy as np
import random
from dotenv import load_dotenv

def convert_km(meter):
    return math.floor(meter / 1000)


def check_in_tabu(move, tabus):
    found = False
    for tabu in tabus:
        if tabu['move'] == move:
            found = True
    return found


class TabuSearch:
    def __init__(self, max_iteration, destinations):
        load_dotenv()
        np.set_printoptions(suppress=True)
        self.max_iteration = max_iteration
        self.can_continue = True
        self.tabu_list = []
        self.initial_distance = 0
        self.max_keep = 100
        self.iteration = 0
        self.iteration_since_reset = 0
        self.api_key = os.getenv('API_KEY')
        self.destinations = destinations
        self.matrix = np.array([])
        self.solution_from_nn = []
        self.distance_from_nn = 0

    def fetch_matrix(self, origin, destinations):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
        params = {
            'key': self.api_key,
            'origins': origin,
            'destinations': destinations,
            'departure_time': 'now',
            'avoid': 'indoor'
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
        return matrix

    def clear_tabu(self):
        if self.max_keep == self.iteration_since_reset:
            if len(self.tabu_list) > 0:
                for idx, tabu in enumerate(self.tabu_list):
                    if tabu['iteration'] == self.iteration - 5:
                        self.tabu_list.pop(idx)
                self.iteration_since_reset = 0
                return
        self.iteration_since_reset += 1

    def swap_move(self, arr):
        copied = copy(arr)
        copied_second = copied[1:len(copied) - 1]
        is_available = False
        total_swap = len(self.destinations) * (len(self.destinations) - 1) / 2
        iteration = 0
        i1, i2 = (0, 0)
        while not is_available and iteration <= total_swap:
            iteration += 1
            i1, i2 = random.sample(copied_second, 2)
            if not check_in_tabu((i1, i2), self.tabu_list) and not check_in_tabu((i2, i1), self.tabu_list):
                is_available = True
        if (i1, i2) == (0, 0):
            self.can_continue = False
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

    @staticmethod
    def find_minimum_distance(solution):
        min_distance = min(data['distance'] for data in solution)
        index = -1
        for idx, data in enumerate(solution):
            if data['distance'] is min_distance:
                index = idx
        return {
            'min_distance': min_distance,
            'index': index,
        }

    def generate_initial_solution(self):
        self.matrix = self.build_matrix()
        print(self.matrix)
        result = [0]
        current = 0
        distance_list = []
        total_distance = 0
        for _ in enumerate(self.destinations):
            if len(result) is len(self.destinations):
                break
            distance_matrix = self.matrix[current]
            prohibited_distance = []
            ok = False
            while not ok:
                min_value = min(i for i in distance_matrix if i > 0 and i not in prohibited_distance)
                at = np.where(distance_matrix == min_value)
                result_index = at[0][0]
                if result_index in result:
                    prohibited_distance.append(min_value)
                    continue
                ok = True
                distance_list.append(min_value)
                result.append(result_index)
                current = result_index
                distance = min_value
                total_distance += distance
        result.append(0)
        print('Initial Solution', result)
        print('Total distance: ', convert_km(self.calculate_distance(result)), 'kilometers')
        print('Total distance in m:', self.calculate_distance(result))
        self.initial_distance = self.calculate_distance(result)
        return result

    def haleluya(self):
        initial_solution = self.generate_initial_solution()
        self.solution_from_nn = copy(initial_solution)
        distance = self.calculate_distance(initial_solution)
        self.distance_from_nn = copy(distance)
        while self.iteration < self.max_iteration:
            # self.clear_tabu()
            neighbourhood = self.generate_neighbourhood(initial_solution)
            if not self.can_continue:
                print('cant continue', self.iteration)
                break
            best_solution = self.find_minimum_distance(neighbourhood)
            if best_solution['min_distance'] < distance:
                self.tabu_list.append({
                    'move': neighbourhood[best_solution['index']]['moves'],
                    'iteration': self.iteration,
                })
                distance = best_solution['min_distance']
                initial_solution = copy(neighbourhood[best_solution['index']]['arr'])
            self.iteration += 1
            print('next iterte', iteration)
        print('final solution tasya', initial_solution)
        print('solution in m:', distance)
        return {
            'solution_from_nn': self.solution_from_nn,
            'distance_from_nn': convert_km(self.distance_from_nn),
            'solution': initial_solution,
            'distance': convert_km(distance),
            'reduction': math.floor(((self.initial_distance - distance) / self.initial_distance) * 100)
        }
