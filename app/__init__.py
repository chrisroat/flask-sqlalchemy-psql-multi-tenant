"""Demonstration of using schema-per-tenant multi-tenant flask app."""
import os

import click
from flask import Flask
from flask_migrate import Migrate

from .data import data_bp
from .models import _init_db, db


class ProdConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite://")


def create_app(config=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    app.register_blueprint(data_bp)
    app.cli.add_command(init_db)
    return app


@click.command("init_db")
def init_db():
    """Initialize the database with global tables."""
    _init_db()
