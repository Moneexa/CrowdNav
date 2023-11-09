from flask import Flask, jsonify, request
from werkzeug.serving import run_simple

app = Flask(__name__)

from app.entitiy.CarRegistry import CarRegistry
from app.routing.CustomRouter import CustomRouter

# Example route for a basic endpoint
@app.route('/')

@app.route('/monitor', methods=['GET'])
def get_monitor_data():
    attributes= {'totalCarCounter': CarRegistry.totalCarCounter, 'totalTripAverage': CarRegistry.totalTripAverage, 'totalTripAvg': CarRegistry.totalTripOverheadAverage}
    data = attributes
    return jsonify(data) 

@app.route('/monitor_schema', methods=['GET'])
def get_monitor_schema_data():
    schema = {
      "type": "object",
      "properties": {
                "totalCarCounter": {"type": "integer"},
                "totalTripAverage": {"type": "number"},
                "totalTripOverheadAverage": {"type": "number"}
        }
    }

    return jsonify(schema)

@app.route('/adaptions_options', methods=['GET'])
def get_adaption_options():
    attributes= {
                   'averageEdgeDurationFactor': CustomRouter.averageEdgeDurationFactor, 
                   'explorationPercentage': CustomRouter.explorationPercentage, 
                   'freshnessCutOffValue': CustomRouter.freshnessCutOffValue, 
                   'freshnessUpdateFactor': CustomRouter.freshnessUpdateFactor, 
                   'maxSpeedAndLengthFactor': CustomRouter.maxSpeedAndLengthFactor,
                   'reRouteEverTicks': CustomRouter.reRouteEveryTicks,
                   'routeRandomSigma': CustomRouter.routeRandomSigma 
                }
    data = attributes
    return jsonify(data) 

@app.route('/adaptions_options_schema', methods=['GET'])
def get_adaptions_options_schema():
    schema= {
        "type": "object",
        "properties": {
                "averageEdgeDurationFactor": {"type": "number"},
                 "explorationPercentage": {"type": "number"},
                 "freshnessCutOffValue": {"type": "integer"},
                 "freshnessUpdateFactor": {"type": "integer"},
                 "maxSpeedAndLengthFactor": {"type": "number"},
                 "reRouteEveryTicks": {"type": "integer"},
                 "routeRandomSigma": {"type": "number"}
            }     
    }
    return jsonify(schema)

@app.route('/execute_schema', methods=['GET'])
def get_execute_schema():
    return jsonify({"type":"object", "properties":{
       "message": "string",
    }})

@app.route('/execute', methods=['PUT'])
def adapt_values():
    data = request.get_json() # Assuming the client sends JSON data

    # Define the keys you expect to be updated
    expected_keys = [
        'averageEdgeDurationFactor',
        'explorationPercentage',
        'freshnessCutOffValue',
        'freshnessUpdateFactor',
        'maxSpeedAndLengthFactor',
        'reRouteEveryTicks',
        'routeRandomSigma'
    ]

    # Initialize a dictionary to store the updates
    updates = {}

    # Check if each expected key is in the data and update accordingly
    for key in expected_keys:
        if key in data:
            updates[key] = data[key]
        else:
            # If the key is not in the data, assign the previous value from CustomRouter
            updates[key] = getattr(CustomRouter, key)

    # Apply the updates to CustomRouter
    CustomRouter.averageEdgeDurationFactor = updates['averageEdgeDurationFactor']
    CustomRouter.explorationPercentage = updates['explorationPercentage']
    CustomRouter.freshnessCutOffValue = updates['freshnessCutOffValue']
    CustomRouter.freshnessUpdateFactor = updates['freshnessUpdateFactor']
    CustomRouter.maxSpeedAndLengthFactor = updates['maxSpeedAndLengthFactor']
    CustomRouter.reRouteEveryTicks = updates['reRouteEveryTicks']
    CustomRouter.routeRandomSigma = updates['routeRandomSigma']

    # Check if all updates were successful (you can customize this logic as needed)
    if all(key in data for key in expected_keys):
        message = "Values updated successfully"
    else:
        message = "Some values were not updated, using previous values"

    return jsonify({"message": message})

def index():
    return 'Hello, this is the root endpoint!'


def runServer():
    run_simple( 'localhost', 5000, app, use_reloader=False, use_debugger=True)
