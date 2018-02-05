from celery.result import EagerResult
from flask import jsonify, abort, request
from covador.flask import json_body

from app import app
from const import OPERATORS

import tasks


def validate_async_result(result):
    if isinstance(result, EagerResult):
        if isinstance(result.result, Exception):
            raise result.result
        return result.result
    else:
        app.logger.error("Not EagerResult")
        abort(500)


@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/stat', methods=['GET'])
def stat():
    result = validate_async_result(tasks.stat.apply_async())
    app.logger.info(f"{result}")
    counts = dict(result)
    return jsonify({title: counts.get(name, 0) for name, title in OPERATORS.items()})


@app.route('/<operator>', methods=['POST'])
@json_body(a=float, b=float)
def multiplying(operator, a, b):
    if operator not in OPERATORS:
        abort(404)
    app.logger.info(f'Operator {operator}')
    result = tasks.operator_task.apply_async(
        (operator, a, b, request.remote_addr))
    result = validate_async_result(result)
    return jsonify({"result": result})
