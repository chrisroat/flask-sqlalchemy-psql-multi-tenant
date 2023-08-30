from flask import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from .models import Data, db

data_bp = Blueprint("data", __name__, url_prefix="/data")


@data_bp.route("/insert/<int:key>/<int:value>", methods=["POST"])
def insert(key, value):
    """Insert a key-value pair into the data table."""
    data = Data(key=key, value=value)
    db.session.add(data)
    try:
        db.session.commit()
    except IntegrityError:
        abort(400)
    return {"status": "success"}


@data_bp.route("/get/<int:key>")
def get(key):
    """Retreive the value for the given `key`."""
    data = db.get_or_404(Data, key)
    return {"value": data.value}
