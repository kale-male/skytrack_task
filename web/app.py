from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from celery import Celery

import os
import logging


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def make_celery(flask_app):
    celery = Celery(flask_app.import_name,
                    backend=flask_app.config['result_backend'],
                    broker=flask_app.config['CELERY_BROKER_URL'],
                    task_always_eager=bool(flask_app.config['CELERY_TASK_ALWAYS_EAGER'])
                    )
    celery.conf.update(flask_app.config)
    celery.conf.update(task_always_eager = True)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# the values of those depend on your setup
DB_URL = get_env_variable("DB_URL")


app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=DB_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    CELERY_BROKER_URL=get_env_variable("CELERY_BROKER_URL"),
    result_backend=get_env_variable("CELERY_RESULT_BACKEND"),
    CELERY_TASK_ALWAYS_EAGER=bool(get_env_variable("CELERY_TASK_ALWAYS_EAGER")))
db = SQLAlchemy(app)


from routes import *

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
