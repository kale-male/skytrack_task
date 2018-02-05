from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.types import IPAddressType

from app import db
from const import OPERATORS


class ArithmLog(db.Model):
    """ """
    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(postgresql.ENUM(
        *OPERATORS.keys(), name='operators'))
    param1 = db.Column(db.Float)
    param2 = db.Column(db.Float)
    result = db.Column(db.Float)
    created = db.Column(db.DateTime)
    ip = db.Column(IPAddressType)
