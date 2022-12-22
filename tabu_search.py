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
        self.matrix = np.array([[0, 180415, 146842, 177227, 163860, 137944, 175868, 172170, 175820,
                                 136687, 141107, 175924, 175275, 179187, 166160, 143521, 191713, 172826, ],
                                [174384, 0, 30018, 13870, 29388, 44354, 7592, 12141, 5338,
                                 39806, 39339, 7533, 5305, 4110, 37627, 22911, 9978, 11187, ],
                                [146794, 28223, 0, 35894, 48836, 19289, 28258, 35640, 28216,
                                 14741, 55225, 28313, 27672, 31584, 57481, 8257, 38068, 33868, ],
                                [174596, 12391, 45561, 0, 18121, 57575, 9937, 3882, 10151,
                                 52451, 40657, 9879, 14326, 8442, 23704, 35555, 12852, 3784, ],
                                [157794, 29264, 48692, 19047, 0, 63028, 17252, 13382, 24668,
                                 58480, 28377, 17194, 24124, 28036, 8673, 41585, 28881, 15205, ],
                                [136322, 46008, 19860, 53679, 66622, 0, 46043, 53425, 46002,
                                 16174, 65853, 46099, 45457, 49369, 74860, 26042, 55853, 51653, ],
                                [169748, 7558, 30070, 9273, 16638, 44406, 0, 7349, 1788,
                                 39858, 34703, 80, 2418, 6330, 23843, 22963, 17016, 5577, ],
                                [166086, 11564, 38132, 5293, 13887, 52468, 8209, 0, 8300,
                                 47920, 31041, 8150, 9270, 7704, 19475, 30321, 15128, 2096, ],
                                [169732, 5423, 29987, 8485, 24735, 44323, 1788, 8154, 0,
                                 39775, 34687, 1729, 1651, 4175, 32974, 22880, 16707, 6382, ],
                                [136471, 40156, 12934, 47828, 60770, 15354, 40192, 47574, 40150,
                                 0, 53112, 40247, 39606, 43518, 69009, 19117, 50002, 45801, ],
                                [135045, 39308, 55214, 36120, 28397, 65246, 34761, 31063, 34712,
                                 53396, 0, 34816, 34168, 38080, 30697, 44429, 45048, 31719, ],
                                [169804, 7500, 30125, 9156, 16902, 44461, 80, 7291, 1729,
                                 39914, 34759, 0, 2360, 6272, 24107, 23019, 18804, 5519, ],
                                [169211, 5482, 29466, 9328, 24214, 43802, 2418, 9188, 1651,
                                 39254, 34166, 2360, 0, 5018, 32453, 22359, 14941, 7416, ],
                                [172997, 4843, 33252, 7035, 28001, 47588, 6204, 8020, 3951,
                                 43040, 37952, 6146, 4916, 0, 26227, 26145, 9810, 6607, ],
                                [160094, 28447, 57013, 25134, 8673, 71349, 24263, 19469, 24655,
                                 66211, 30677, 24205, 32445, 36357, 0, 49906, 34969, 21292, ],
                                [143444, 23843, 9869, 31515, 44457, 24205, 23878, 31261, 23837,
                                 17135, 40158, 23934, 23293, 27204, 52696, 0, 33689, 29488, ],
                                [186853, 9548, 39863, 11321, 29342, 54199, 18844, 15104, 16591,
                                 49651, 50592, 18786, 14763, 9946, 34925, 32756, 0, 13581, ],
                                [166582, 9685, 36253, 5228, 16190, 50639, 6514, 2096, 6420,
                                 46041, 31537, 6456, 7390, 5824, 21773, 28619, 13620, 0]])
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
        # if len(self.matrix) == 0:
        #     self.matrix = self.build_matrix()
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
        self.iteration = 0
        self.tabu_list = []
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
            print('iterate', self.iteration)
        print('final solution tasya', initial_solution)
        print('solution in m:', distance)
        return {
            'solution_from_nn': self.solution_from_nn,
            'distance_from_nn': convert_km(self.distance_from_nn),
            'solution': initial_solution,
            'distance': convert_km(distance),
            'reduction': math.floor(((self.initial_distance - distance) / self.initial_distance) * 100)
        }
