from ..entitiy.CarRegistry import CarRegistry
import json
from bottle import Bottle, request, response


from ..routing.CustomRouter import CustomRouter
app = Bottle()

@app.route('/')
def index():
    return 'Hello, this is the root endpoint!'

@app.route('/monitor', method='GET')
def get_monitor_data():
    attributes = {
        'totalCarCounter': CarRegistry.totalCarCounter,
        'totalTripAverage': CarRegistry.totalTripAverage,
        'totalTripOverheadAverage': CarRegistry.totalTripOverheadAverage
    }
    data = attributes
    response.content_type = 'application/json'
    return json.dumps(data)

@app.route('/monitor_schema', method='GET')
def get_monitor_schema_data():
    schema = {
        "type": "object",
        "properties": {
            "totalCarCounter": {"type": "integer"},
            "totalTripAverage": {"type": "number"},
            "totalTripOverheadAverage": {"type": "number"}
        }
    }
    response.content_type = 'application/json'
    return json.dumps(schema)

@app.route('/adaptions_options', method='GET')
def get_adaption_options():
    attributes = {
        'averageEdgeDurationFactor': CustomRouter.averageEdgeDurationFactor,
        'explorationPercentage': CustomRouter.explorationPercentage,
        'freshnessCutOffValue': CustomRouter.freshnessCutOffValue,
        'freshnessUpdateFactor': CustomRouter.freshnessUpdateFactor,
        'maxSpeedAndLengthFactor': CustomRouter.maxSpeedAndLengthFactor,
        'reRouteEveryTicks': CustomRouter.reRouteEveryTicks,
        'routeRandomSigma': CustomRouter.routeRandomSigma
    }
    response.content_type = 'application/json'
    return json.dumps(attributes)

@app.route('/adaptions_options_schema', method='GET')
def get_adaptions_options_schema():
    schema = {
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
    response.content_type = 'application/json'
    return json.dumps(schema)

@app.route('/execute_schema', method='GET')
def get_execute_schema():
    schema = {"type": "object", "properties": {"message": "string"}}
    response.content_type = 'application/json'
    return json.dumps(schema)

@app.route('/execute', method='PUT')
def adapt_values():
    data = json.load(request.body)  # Assuming the client sends JSON data

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

    response.content_type = 'application/json'
    return json.dumps({"message": message})

def run_server():
    app.run(host='localhost', port=5000, reloader=False, debug=True)