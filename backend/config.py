import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_user = 'udacity'
database_pwd = 'udacity'
database_server = 'localhost'
database_name = 'udacity_trivia'
database_port = '5438'
database_path = 'postgresql://{}:{}@{}:{}/{}'.format(database_user, database_pwd,database_server, database_port, database_name)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_SERVER_URI = 'postgresql://{}:{}@{}:{}'.format(
    database_user, database_pwd, database_server, database_port)
