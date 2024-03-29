# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.9.17** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:
```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal log in the database shell:
```bash
psql "dbname=<DB_NAME> host=<SERVER> user=<USER_NAME> password=<PWD> port=<PORT> sslmode=<ARGS>"
```

then populate the data from the trivia.sql file:
```bash
psql trivia < trivia.psql
```

Finally create a `trivia_test` database for integratiuon and unit testing:
```bash
createdb trivia_test
```

### Set up the environment
[Python-dotenv](https://pypi.org/project/python-dotenv/) is the package that will handle loading the environment to prevent hardcoding the configuration values. The `.env` file in the backend's root directory allows for easy configuration of the environment during development, or production. The `.env.test` file handles the connection to the test database for the unit tests.

`These files should NOT be included in source control system to prevent unauthorized access`

The required environment variables are: 
- SECRET_KEY: a string value unused at this time. Could be used to implement basic key authorization for the endpoints  
- DEBUG: a boolean value used for debugging purposes
- DB_SRV: the url of the server that hosts the database (e.g.: localhost)
- DB_NAME: the name of the database (e.g.: udacity_trivia)
- DB_PORT: the port the server is listening to (default: 5438)
- DB_USER: The username that has read, connection, and write permissions to the database
- DB_PWD = the user password
- TRACK_MODS: a flag to enable or disable SQLAlchemy tracking modifications of objects. Maps to SQLALCHEMY_TRACK_MODIFICATIONS. Set it to False to disable tracking and use less memory. Defaults to FALSE if not set.
- DATABASE_URI: the full uri for postgeSQL in the following format: postgresql://${DB_USER}:${DB_PWD}@${DB_SRV}:${DB_PORT}/${DB_NAME}





### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

Alternatively, if you're using VS Code, you could just run and debug using the configuration  in `.vscode/launch.json`

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Endpoint documentation

Detailed documentation of the API endpoints including the URL, request parameters, and the response body can be found in the `DOCUMENTATION.md` file.

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb <DB_NAME>_test
createdb <DB_NAME>_test
psql <DB_NAME>_test < trivia.psql
python test_flaskr.py
```
