from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DDL

db = SQLAlchemy()


class Tenant(db.Model):
    """A tenant is identified by its domain and its assigned schema."""

    # Bound to the db engine that handles non-tenant schema.
    __bind_key__ = "global"

    domain = db.Column(db.String(1024), primary_key=True)
    schema = db.Column(db.String(256), unique=True, nullable=False)


class Data(db.Model):
    """Simple key-value model."""

    # Bound to the db engine that handles per-user schemas.
    __bind_key__ = "per_user"

    # The schema should always be updated to the tenant's schema using the
    # schema_translate_map of the engine's execution options.
    __table_args__ = {"schema": "per_user"}

    key = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)


def _init_db():
    """Create the non-tenant tables."""
    db.create_all(bind_key="global")


def _add_tenant(domain, schema):
    """Create a new tenant, their schema, and their tables."""
    db.session.connection().execute(
        DDL("CREATE SCHEMA IF NOT EXISTS %(schema)s", {"schema": schema})
    )
    db.session.commit()
    db.session.add(Tenant(domain=domain, schema=schema))
    db.session.commit()

    with PerUserSchema(domain):
        db.create_all(bind_key="per_user")


class PerUserSchema:
    """Utility to help set the schema for a"""

    def __init__(self, domain):
        self.domain = domain
        self.orig_map = None

    def set(self):
        """Set the per-user engine to use the tenant schema."""
        tenant = db.get_or_404(Tenant, self.domain)
        tmap = {"per_user": tenant.schema}
        db.engines["per_user"].update_execution_options(schema_translate_map=tmap)

    def __enter__(self):
        """Set the schema when enter as a context-manager."""
        self.orig_map = (
            db.engines["per_user"].get_execution_options().get("schema_translate_map")
        )
        self.set()

    def __exit__(self, *args, **kwargs):
        """Reset the schema when exiting as a context-manager."""
        db.engines["per_user"].update_execution_options(
            schema_translate_map=self.orig_map
        )
