from app import create_app, db
from app.models import User, Registration, Payment
import click
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Registration': Registration,
        'Payment': Payment
    }

@app.cli.command("create-admin")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_admin(username, email, password):
    """Create an admin user"""
    try:
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin user {username} created successfully")
    except Exception as e:
        click.echo(f"Error creating admin user: {str(e)}")

@app.cli.command("init-db")
def init_db():
    """Initialize the database and create required directories."""
    try:
        with app.app_context():
            db.create_all()
            # Create upload directory if it doesn't exist
            uploads_dir = app.config['UPLOAD_FOLDER']
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            click.echo('Database initialized and upload directory created.')
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")

@app.cli.command("reset-db")
def reset_db():
    """Reset the database."""
    if click.confirm('Are you sure you want to reset the database?'):
        with app.app_context():
            db.drop_all()
            db.create_all()
            click.echo('Database has been reset.')

if __name__ == "__main__":
    with app.app_context():
        try:
            # Ensure database tables exist
            db.create_all()
            
            # Ensure upload directory exists
            uploads_dir = app.config['UPLOAD_FOLDER']
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
                
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            
    app.run(debug=True)
