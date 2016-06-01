"""
Alembic migration management file
"""
import os
import sys
PROJECT_HOME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_HOME)
from app import create_app
from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from models import db, Article, Citations

# Load the app with the factory
app = create_app()


class BuildDatabase(Command):
    """
    Build the Article-Citations-Sentiment database
    """
    @staticmethod
    def run(app=app):
        pass


# Set up the alembic migration
migrate = Migrate(app, db, compare_type=True)

# Setup the command line arguments using Flask-Script
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
