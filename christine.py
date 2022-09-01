import os
from copy import copy
from time import time
import requests

class Christine:
    def __init__(self, destinations, solution, loading_time):
        self.destinations = destinations
        self.solution = solution
        self.loading_time = loading_time
        self.api_key = os.getenv('API_KEY')

    def fetch_time(self, origin, destination, departure_time):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
        params = {
            'key': self.api_key,
            'origins': origin,
            'destinations': destination,
            'departure_time': departure_time,
        }
        resp = requests.get(url, params=params)
        time_seconds = resp.json()['rows'][0]['elements'][0]['duration']['value']
        return time_seconds

    def haleluya(self):
        now = int(time())
        copied_now = copy(now)
        duration_arr = []
        timestamp_arr = []
        for i in range(len(self.solution)):
            if i == len(self.solution) - 1:
                break
            fetched_time = self.fetch_time(self.destinations[self.solution[i]], self.destinations[self.solution[i + 1]],
                                           now)
            now += fetched_time
            duration_arr.append(fetched_time)
            timestamp_arr.append(now)
            now += self.loading_time * 60
        return {
            'duration_arr': duration_arr,
            'timestamp_arr': timestamp_arr,
            'now': copied_now,
        }
