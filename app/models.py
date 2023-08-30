from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Data(db.Model):
    """Simple key-value model."""

    key = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)


def _init_db():
    """Create the non-tenant tables."""
    db.create_all()
