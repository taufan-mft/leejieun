from tabu_search import TabuSearch
import math

class Jeanice:
    def __init__(self, efficiency, max_duration, petrol_price, capacity, destinations):
        self.efficiency = efficiency
        self.max_duration = max_duration
        self.petrol_price = petrol_price
        self.capacity = capacity
        self.destinations = destinations

    def calculate_petrol_price(self, distance):
        consumed = math.ceil(distance/self.efficiency)
        price = consumed * self.petrol_price
        return price

    def haleluya(self):
        ts = TabuSearch(max_iteration=500, destinations=self.destinations)
        min_distance = 99999999999
        best_solution = None
        for i in range(3):
            current_solution = ts.haleluya()
            if current_solution['distance'] < min_distance:
                best_solution = current_solution
                min_distance = current_solution['distance']
        solution, distance, reduction = best_solution.values()
        petrol_price = self.calculate_petrol_price(distance)
        return {
            'solution': solution,
            'distance': distance,
            'petrol_price': petrol_price,
            'reduction': reduction,
        }
