from tabu_search import TabuSearch
import math

class Jeanice:
    def __init__(self, efficiency, max_duration, petrol_price, capacity, destinations, max_iteration):
        self.efficiency = int(efficiency)
        self.max_duration = int(max_duration)
        self.petrol_price = int(petrol_price)
        self.capacity = int(capacity)
        self.destinations = destinations
        self.max_iteration = int(max_iteration)

    def calculate_petrol_price(self, distance):
        consumed = math.ceil(distance/self.efficiency)
        price = consumed * self.petrol_price
        return price

    def haleluya(self):
        ts = TabuSearch(max_iteration=self.max_iteration, destinations=self.destinations)
        min_distance = 99999999999
        best_solution = None
        for i in range(5):
            current_solution = ts.haleluya()
            if current_solution['distance'] < min_distance:
                best_solution = current_solution
                min_distance = current_solution['distance']
        solution_from_nn, distance_from_nn, solution, distance, reduction = best_solution.values()
        petrol_price = self.calculate_petrol_price(distance)
        return {
            'solution_from_nn': solution_from_nn,
            'distance_from_nn': distance_from_nn,
            'solution': solution,
            'distance': distance,
            'petrol_price': petrol_price,
            'reduction': reduction,
        }
