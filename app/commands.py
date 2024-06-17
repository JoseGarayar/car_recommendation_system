from flask import current_app
from flask.cli import with_appcontext
import click
from models import User
from __init__ import db

@click.command(name='create-user')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_user(username, email, password):
    """Create a new user."""
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} created successfully.")

def register_commands(app):
    app.cli.add_command(create_user)