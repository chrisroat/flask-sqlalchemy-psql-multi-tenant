"""Demonstration of using schema-per-tenant multi-tenant flask app."""
import os

import click
from flask import Flask, request
from flask_migrate import Migrate

from .data import data_bp
from .models import PerUserSchema, _add_tenant, _init_db, db


class ProdConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite://")

    # Separate binds are made so that global and per-user tables can be
    # accessed independently.  All binds reference the same URI.
    SQLALCHEMY_BINDS = {
        "global": SQLALCHEMY_DATABASE_URI,
        "per_user": SQLALCHEMY_DATABASE_URI,
    }


def create_app(config=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    app.register_blueprint(data_bp)
    app.cli.add_command(init_db)
    app.cli.add_command(add_tenant)

    @app.before_request
    def before_request():
        # Set up binding so that `db` will reference per-user tables
        # in the schema corresponding to the host of this `request`.
        PerUserSchema(request.host).set()

    return app


@click.command("init_db")
def init_db():
    """Initialize the database with global tables."""
    _init_db()


@click.command("add_tenant")
@click.argument("domain")
@click.argument("schema")
def add_tenant(domain, schema):
    """Add new tenant, creating its schema and tables."""
    _add_tenant(domain, schema)
