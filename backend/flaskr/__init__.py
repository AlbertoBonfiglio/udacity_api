import os
import sys
from flask import Flask, request, abort, jsonify, make_response
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, func
from sqlalchemy import exc
from werkzeug import exceptions
from flask_cors import CORS, cross_origin
import random
from models import setup_db, db,  Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db.session.expire_all()

    """
    #TODO [X]: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    
    """
    # TODO [X]: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    
    """
    #TODO [ ]: Create an endpoint to handle GET requests for all available categories.
    """
    @app.route('/api/v1.0/categories', methods=['GET'])
    @cross_origin()
    def get_categories():
        try: 
            data = Category.query.all()
            formattedData = [datum.format() for datum in data]
            # returns the formatted data or an empty array
            return jsonify({
            'success': True,
            'data': formattedData   
            })
            
        except Exception as err:
            print(err)
            return "Internal error", status.HTTP_500_INTERNAL_SERVER_ERROR

        
    """
    #TODO [X]: Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1.0/questions', methods=['GET'])
    @cross_origin()
    def get_questions():
        try:
            # gets the params 
            pageNumber = request.args.get('page', 1, type=int)
            itemsPerPage = request.args.get('perPage', QUESTIONS_PER_PAGE, type=int)
            categoryId = request.args.get('category', -1, type=int)
            
            # retrieves the appropriate data
            if (categoryId != -1):
                # makes sure we get a valid category if one is passed in
                categoryObj = Category.query.get(categoryId)
                if (categoryObj == None):
                    return "Database error. Category not found", status.HTTP_404_NOT_FOUND
                else:
                    categoryObj = categoryObj.format()
                result = Question.query \
                    .filter(Question.category == categoryId ) \
                    .paginate(page=pageNumber, per_page = itemsPerPage)
            else:
                categoryObj = None
                # errors if invalid pagenumber
                result = Question.query.paginate(page = pageNumber, per_page = itemsPerPage)
            
            # formats the data for output    
            formattedData = [datum.format() for datum in result.items]
            
            # gets the available categories. Returns an error if it can't find any
            categoryData = Category.query.all()
            if (categoryData == None):
                return "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR
            formattedCategoryData = [datum.format() for datum in categoryData]
            
            # formats the response
            return jsonify({
             'success': True,
             'data': formattedData,   
             'total': result.total ,
             'category': categoryObj,
             'categories': formattedCategoryData,
             'page': pageNumber,
             'pages': result.pages,
             'perPage': itemsPerPage
            })
        
        except exceptions.NotFound:
            # If the page is outside the boundaries sqlalchemy returns: 
            # werkzeug.exceptions.NotFound: 404 Not Found: The requested URL was not found on the server.
            return "Database error. Page outside limits.", status.HTTP_404_NOT_FOUND
        
        except Exception as err:
            print(sys.exc_info(), err)
            return "Internal error", status.HTTP_500_INTERNAL_SERVER_ERROR
        
    
    """
    #TODO [X]: Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def delete_question(question_id=int):
        try:
            record: Question = Question.query.get(question_id)
            if (record == None):
               return f'Question # {question_id} not found.', status.HTTP_404_NOT_FOUND
            
            record.delete();
            return f'Question # {question_id} has been successfully deleted.', status.HTTP_200_OK
      
        except Exception as err:
            print(sys.exc_info(), err)
            return 'Internal Server Error', status.HTTP_500_INTERNAL_SERVER_ERROR
  


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
