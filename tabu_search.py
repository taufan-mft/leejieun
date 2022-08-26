import requests
import numpy as np

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
                             '-7.396291,109.265564']

    def fetch_matrix(self, number_of_destinations, origin, destinations):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
        params = {
            'key': self.api_key,
            'origins': origin,
            'destinations': destinations,
        }
        resp = requests.get(url, params=params)
        received_array = resp.json()['rows'][0]['elements']
        holder = np.zeros((1, number_of_destinations))
        temp = []
        for index, data in enumerate(received_array):
            temp.append(data['distance']['value'])

        holder[0] = temp
        return temp

    def build_matrix(self):
        origin = '40.6655101,-73.8918896999999'
        number_of_destinations = len(self.destinations)
        parsed_destinations = '|'.join(map(str, self.destinations))
        matrix = np.zeros((number_of_destinations, number_of_destinations))
        for idx, destination in enumerate(self.destinations):
            result = self.fetch_matrix(number_of_destinations, destination, parsed_destinations)
            matrix[idx] = result
        print(matrix)
        return matrix

    def generate_initial_solution(self):
        matrix = self.build_matrix()
        result = []
        current = 0
        distance = 0
        for idx, destination in enumerate(self.destinations):
            distance_matrix = matrix[current]
            min_value = min(i for i in distance_matrix if i > 0 and i != distance)
            at = np.where(distance_matrix == min_value)
            result_index = at[0][0]
            result.append(result_index)
            current = result_index
            distance = min_value
        print(result)


tasya = TabuSearch(max_iteration=5, number_of_customer=2)
tasya.generate_initial_solution()
