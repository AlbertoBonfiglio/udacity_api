import os
import sys
from dotenv import load_dotenv


def load_config(env=".env"):
    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    load_dotenv(os.path.join(basedir, env))

    try:  # Makes sure the environment is configured
        try:  # If variable does not exists sets a default
            SECRET_KEY = os.environ["SECRET_KEY"]
        except Exception as err:
            SECRET_KEY = os.urandom(32)

        # Enable debug mode.
        try:  # If variable does not exists sets a default
            DEBUG = os.environ['DEBUG']
        except Exception as err:
            DEBUG = False

        try:
            TRACK_MODS = os.environ['TRACK_MODS']
        except Exception as err:
            TRACK_MODS = False

        DATABASE_URI = os.environ['DATABASE_URI']

    except Exception as err:
        # Log the error to the console
        print("Error retrieving configuration values: ", err)
        # rethrow it
        sys.exit(1)
