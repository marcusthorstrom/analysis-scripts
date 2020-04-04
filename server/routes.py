from server import app
from server.invalid_usage import InvalidUsage
from flask import jsonify, request, abort, make_response

from analysis.utils.factory import IndividualReportFactory
from analysis.utils.db import session
from analysis.utils.db import LocationModel, IndividualReportModel


import sys

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/locations', methods=['GET'])
def all_locations():
    q = session.query(LocationModel)
    locations = q.all()
    return jsonify(locations= [loc.serialize() for loc in locations])

@app.route('/reports', methods=['GET'])
def all():
    q = session.query(IndividualReportModel)
    individuals = q.all()
    return jsonify(individials= [individual.serialize() for individual in individuals])

@app.route('/<int:id>', methods=['GET'])
def get(id):
    return jsonify([id])

@app.route('/add-person', methods=['POST'])
def add_person():
    if not request.json:
        raise InvalidUsage("No data supplied")
    
    param_list = ['id', 'data']
    check_param(request.json, param_list)

    data_list = ['diagnostic', 'locator', 'sessionId', 'timestamp']
    check_param(request.json['data'], data_list)
    
    timestamp_list = ["_seconds", "_nanoseconds"]
    check_param(request.json['data']['timestamp'], timestamp_list)


    try:
        report = IndividualReportFactory.build(request.json)
        try:
            session.add(report)
            session.commit()
        except:
            session.rollback()
            print("Could not insert to database")
            abort(500)
    except TypeError:
        raise InvalidUsage("Some parameter was wrongly typed (string, int, array).")
    except:
        print("Could not create Individual Report. Probably malformed json. JSON:{%s}, %s", request.json)
        abort(400)


def check_param(obj, param_list):
    for param in param_list:
        if (not param in obj) or (obj[param] == None):
            raise InvalidUsage("parameter '%s' is not supplied" % param)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response