# -*- coding: utf-8 -*-

"""
    nbx.commands
    ~~~~~~~~~~~~

    :copyright: (c) 2016 by Augusto Roccasalva
    :license: GPLv3, see LICENSE for more details.
"""

import click

from nbx.application import create_app
from nbx.models import db, User, Email


app = create_app()

@app.cli.command()
@click.option('--username')
@click.option('--password')
@click.option('--email')
@click.option('--role')
def createuser(username, password, email, role):
    """Create a new user interactivelly"""

    if username is None:
        while True:
            username = click.prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                click.echo("Username {} already exists.".format(username))
            else:
                break

    if email is None:
        while True:
            email = click.prompt("Email address")
            exists = Email.query.filter(Email.email==email).first()
            if exists is not None:
                click.echo("Email {} already exists.".format(email))
            else:
                break

    if password is None:
        password = click.prompt("Password", hide_input=True,
                                confirmation_prompt=True)

    first_name = click.prompt("First name (required)")
    last_name = click.prompt("Last name")

    roles = {
        "member": User.MEMBER,
        "moderator": User.MODERATOR,
        "admin": User.ADMIN,
    }

    if role is None:
        role = click.prompt("Role", default="memeber",
                            type=click.Choice(roles.keys()))

    user = User(username=username, password=password, role=roles[role],
                first_name=first_name, last_name=last_name)
    email_addr = Email(email_type="Main", email=email)
    user.email.append(email_addr)

    db.session.add(user)
    db.session.commit()

    click.echo("User created with ID {}".format(user.id))


@app.cli.command()
def initdb():
    """Creates database tables"""
    db.create_all()


@app.cli.command()
def dropdb():
    """Drops all databse tables"""
    if click.confirm('Are you sure? You will lose all your data!'):
        db.drop_all()


@app.cli.command()
def loadfix():
    """Load fixtures located in fixtures files."""
    import os.path
    import glob
    from nbx.utils.fixtures import load_yaml, load_fixtures
    if click.confirm('Are you sure? You will lose all your data!'):
        db.drop_all()
        db.create_all()

        for fixture_dir in app.config.get('FIXTURES_DIRS', ['./tests/fixtures/']):
            for fixture_file in glob.glob(fixture_dir + '/*.yaml'):
                print("loading fixtures from '{}'".format(fixture_file))
                fixtures = load_yaml(fixture_file)
                load_fixtures(db, fixtures)


@app.cli.command()
def migrate():
    """Migrate from a database for old application"""
    from nbx.utils.migrate import migrate_suppliers, configure_session
    db.create_all()
    session = configure_session(app.config['MIGRATION_DB_URI'])
    migrate_suppliers(session)
