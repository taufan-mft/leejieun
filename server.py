import json
from flask import Flask, jsonify, request
from markupsafe import escape
from jeanice import Jeanice
from christine import Christine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def convert_to_id(beginning, solution, map_dest):
    temp = []
    for item in solution:
        for data in beginning:
            if data['lat_lng'] == map_dest[item]:
                temp.append(data['id'])
    return temp

@app.route("/jeanice", methods=['POST'])
def hello():
    data = json.loads(request.data)
    petrol_price = data['petrol_price']
    num_iteration = data['num_iteration']
    max_duration = data['max_duration']
    efficiency = data['efficiency']
    destinations = data['destinations']
    loading_time = int(data['loading_time'])
    map_dest = [destination['lat_lng'] for destination in destinations]
    jeanice = Jeanice(destinations=map_dest, capacity=700, efficiency=efficiency, max_duration=max_duration,
                      petrol_price=petrol_price, max_iteration=num_iteration)
    solution = jeanice.haleluya()
    christine = Christine(map_dest, solution['solution'], loading_time)
    time_manager = christine.haleluya()
    return jsonify({
        'status': 'OK',
        'solution': str(solution['solution']),
        'solution_id': convert_to_id(destinations, solution['solution'], map_dest),
        'distance': int(solution['distance']),
        'petrol_price': solution['petrol_price'],
        'reduction': solution['reduction'],
        **time_manager,
    })


@app.route('/tasya', methods=['POST'])
def tasya():
    data = json.loads(request.data)
    destinations = data['destinations']
    map_dest = [destination['lat_lng'] for destination in destinations]
    print(map_dest)
    return jsonify({
        'status': 'OK'
    })
