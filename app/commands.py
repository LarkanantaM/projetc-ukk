from flask import current_app
from flask.cli import with_appcontext
import click
from app import db

@click.command('reset-db')
@with_appcontext
def reset_db():
    """Reset the database."""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        db.create_all()
        click.echo('Database has been reset.')