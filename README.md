# Flask+SqlAlchemy+Postgres+MultiTenancy

Example of a per-schema multi-tenant flask-sqla app using postgres backend.

The initial commit of the repo is a single-tenant app containing a simple key-value store.
The second commit contains updates to support
multi-tenant schema.
Each tenant is tied to a hostname and has data stored in a
separate schema.

Because this recipe uses multiple schemas, it requires a [PostgreSQL](https://www.postgresql.org/) backend.

TODO: Update alembic scripts to demonstrate multi-tenant schema versioning.

## Local demonstration

Create an empty database.  The default user in this example has no
password and can create a database -- modify for your user as needed.

    $ psql
    ...
    {user}=# create database multitenant;
    CREATE DATABASE
    {user}=# \quit
    $ export DATABASE_URL="postgresql://localhost/multitenant"

Clone the repo and install dependencies:

    $ git clone git@github.com:chrisroat/flask-sqlalchemy-psql-multi-tenant.git
    ...
    $ virtualenv venv
    created virtual environment ...
    $ source venv/bin/activate
    ...
    $ pip install -r requirements.txt
    ...

Using custom CLI commands, set up the database with two tenants referring
to different hostnames of a local app.  Then launch the app:

    $ flask init_db
    $ flask add_tenant 127.0.0.1:5000 ip
    $ flask add_tenant localhost:5000 local
    $ DATABASE_URL="postgresql://localhost/multitenant" flask run --debug
    ...

Demonstrate:

    # Insert data using one tenant.
    $ curl -X POST http://127.0.0.1:5000/data/insert/42/8675309
    {
      "status": "success"
    }

    # Retreive data from the same tenant.
    $ curl http://127.0.0.1:5000/data/get/42
    {
      "value": 8675309
    }

    # Cannot retreive data from second tenant.
    $ curl http://localhost:5000/data/get/42
    <!doctype html>
    <html lang=en>
    <title>404 Not Found</title>
    <h1>Not Found</h1>
    <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

## Testing

Testing is done on a local database host, using access given
by a user/password which can manage databases.  Note that
`TEST_DB_HOST` differs from `DATABASE_URL` in that it lacks
a database name.

    TEST_DB_HOST="postgresql://myuser" python -m pytest
``
