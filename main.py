tasya = [{'moves': (1, 2), 'arr': [0, 3, 2, 1, 0], 'distance': 7316.0},
         {'moves': (2, 3), 'arr': [0, 2, 1, 3, 0], 'distance': 7317.0},
         {'moves': (1, 3), 'arr': [0, 1, 3, 2, 0], 'distance': 10505.0},
         {'moves': (3, 1), 'arr': [0, 1, 3, 2, 0], 'distance': 10505.0},
         {'moves': (1, 3), 'arr': [0, 1, 3, 2, 0], 'distance': 10505.0}]
print(min(data['distance'] for data in tasya))
