import sys
import random

from flask import Flask, request, abort, jsonify, make_response
from flask_api import status
from werkzeug import exceptions
from flask_cors import CORS, cross_origin
from backend.models import setup_db, db,  Question, Category

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
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    #TODO [X]: Create an endpoint to handle GET requests for all available categories.
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
            return internal_error(err)

    @app.route('/api/v1.0/categories/<int:categoryId>', methods=['GET'])
    @cross_origin()
    def get_category(categoryId= int):
        try:
           
            # retrieves the appropriate category data 
            # (eventually refactor to own function or lambda)
            category: Category = Category.query.get(categoryId)
                
            if (category == None):
                return unprocessable("Category does not exist")

            
            formattedData = category.format()

            return jsonify({
                'success': True,
                'data': formattedData
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

    @app.route('/api/v1.0/categories/<int:categoryId>/questions', methods=['GET'])
    @cross_origin()
    def get_questions_by_category2(categoryId= int):
        try:
           
            # retrieves the appropriate category data 
            # (eventually refactor to own function or lambda)
            category: Category = Category.query.get(categoryId)
                
            if (category == None):
                return unprocessable("Category does not exist")

            result = Question.query \
                .order_by(Question.id.asc()) \
                .filter(Question.category == category.id) \
                .all()

            formattedData = [datum.format() for datum in result]

            return jsonify({
                'success': True,
                'category': category.format(),
                'data': formattedData
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)


    """
    #TODO [X]: Create an endpoint to handle GET requests for questions, including pagination 
    (every 10 questions).    
    This endpoint should return a list of questions, number of total questions, current category, categories.
    
    TEST: At this point, when you start the application you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1.0/questions', methods=['GET'])
    @cross_origin()
    def get_questions():
        try:
            # gets the params
            pageNumber = request.args.get('page', 1, type=int)  # type: ignore
            itemsPerPage = request.args.get(
                'perPage', QUESTIONS_PER_PAGE, type=int)  # type: ignore
            categoryId = request.args.get(
                'category', None, type=int)  # type: ignore

            # retrieves the appropriate data
            query = Question.query.order_by(Question.id.asc())
            if (categoryId != None):
                # makes sure we get a valid category if one is passed in
                categoryObj = Category.query.get(categoryId)
                if (categoryObj == None):
                    return unprocessable("Database error. Category not found.")
                categoryObj = categoryObj.format()
                query = query.filter(Question.category == categoryId)
            else:
                categoryObj = None

            # errors if invalid pagenumber
            result = query.paginate(page=pageNumber, per_page=itemsPerPage)

            # formats the data for output
            formattedData = [datum.format() for datum in result.items]

            # gets the available categories. Returns an error if it can't find any
            categoryData = Category.query.all()
            if (categoryData == None):
                raise Exception(
                    'Database error. Unable to retrieve categories')
            formattedCategoryData = [datum.format() for datum in categoryData]

            # formats the response
            return jsonify({
                'success': True,
                'data': formattedData,
                'total': result.total,
                'category': categoryObj,
                'categories': formattedCategoryData,
                'page': pageNumber,
                'pages': result.pages,
                'perPage': itemsPerPage
            })

        except exceptions.NotFound:
            # If the page is outside the boundaries sqlalchemy returns:
            # werkzeug.exceptions.NotFound: 404 Not Found: The requested URL was not found on the server.
            return not_found("Database error. Page outside limits.")

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

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
                return not_found(f'Question # {question_id} not found.')

            record.delete()
            return f'Question # {question_id} has been successfully deleted.', status.HTTP_200_OK

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

    """
    #TODO [X]: Create an endpoint to POST a new question, which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at 
    the end of the last page of the questions list in the "List" tab.
    """
    @app.route('/api/v1.0/questions', methods=['POST'])
    @cross_origin()
    def post_question():
        try:
            body = request.get_json()  # type: ignore

            # checks the category
            category = Category.query.get(body.get('category', None))
            if (category == None):
                return unprocessable('Invalid data [category not found]')

            # builds the record
            question = body.get('question', '').strip()
            answer = body.get('answer', '').strip()
            
            record: Question = Question(
                question= question,
                answer = answer,
                category = category.id,
                difficulty = body.get('difficulty', 0)
            )
            if (record.question != '' and record.answer != '' ):
                record.insert()
            else:
                return unprocessable('Invalid data [question or answer]')

            return jsonify({
                'success': True,
                'data': record.format()
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

    """
    #TODO [X]: Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term  is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include  only question that 
    include that string within their question.  Try using the word "title" to start.
    """
    @app.route('/api/v1.0/questions/search', methods=['POST'])
    @cross_origin()
    def find_questions():
        try:
            body = request.get_json()  # type: ignore
            search = body.get('search', None)

            if (search == None):
                return unprocessable('No search string provided')

            # cleans up the string    
            search = search.strip()
            result = []
            if (search != '') : # No point serarching for nothing
                result = Question.query \
                    .filter(Question.question.ilike(f'%{search}%')) \
                    .all()

            formattedData = [datum.format() for datum in result]

            return jsonify({
                'success': True,
                'query': search,
                'data': formattedData,
                'found': len(formattedData)
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)


    """
    #TODO [X]: Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1.0/questions/category', methods=['GET'])
    @cross_origin()
    def get_questions_by_category():
        try:
            qry = Category.query
            
            categoryId = request.args.get('id', None, type=int)  # type: ignore
            categoryType: str = request.args.get('type', None, type=str)  # type: ignore
            
            if (categoryId == None and categoryType == None ):
                return unprocessable("Bad category arguments")
            
            # retrieves the appropriate category data 
            # (eventually refactor to own function or lambda)
            if (categoryType == None ):
                category: Category = qry.get(categoryId)
                
            if (categoryId == None):
                # gets the first item matching or None
                list = qry \
                    .filter(Category.type.ilike(f'%{categoryType}%')) \
                    .all()
                category: Category = list[0] if list else None 
            if (category == None):
                return unprocessable("Category does not exist")

            result = Question.query \
                .order_by(Question.id.asc()) \
                .filter(Question.category == category.id) \
                .all()

            formattedData = [datum.format() for datum in result]

            return jsonify({
                'success': True,
                'category': category.format(),
                'data': formattedData
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)


    

    """
    #TODO [X]: Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random question within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/v1.0/questions/random', methods=['POST'])
    @cross_origin()
    def get_random_questions():
        try:
            qry = Question.query
            body = request.get_json()  # type: ignore
            category: int = body.get('category', None)
            previous: [int] = body.get('previous', [])
            
            # if a category is specified filters the resultset
            if (category != None):
                category: Category = Category.query.get(category)
                if (category == None):                
                    return unprocessable("Category does not exist")
                qry = qry.filter(Question.category == category.id)
                        
            # filters out previous questions if necessary
            if (previous):
                qry = qry.filter(Question.id.notin_(previous))  
                #TODO [ ] Maybe at a later time verify that all the passed in previous
                #         ids actually exists and remove the invalid ones from the list
                #         For right now we just ignore them

            # gets the data
            # this disregards the possibility of invalid previous entries
            result = qry.all()
            available = len(result) 
            if (result): # something is returned
                available = available - 1 # left over questions in category
                rando: Question = random.choice(result)
                formattedData = rando.format()
                previous.append(rando.id)
            else:
                formattedData = None

            return jsonify({
                'success': True,
                'category': category.format() if category else None,
                'previous': previous,  
                'data': formattedData,
                'available': available 
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)
        
    
    """
    #TODO [X]:
    Create error handlers for all expected errors including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": str(error),
            "message": "Not found"
        }), status.HTTP_404_NOT_FOUND

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": error,
            "message": "Not allowed"
        }), status.HTTP_405_METHOD_NOT_ALLOWED
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": error,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_error(error: Exception):
        return jsonify({
            "success": False,
            "error": error.args[0],
            "message": "Internal Server Error"
        }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return app
