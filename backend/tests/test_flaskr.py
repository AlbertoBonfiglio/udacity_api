import os
import unittest
import json
import math
from backend.config import load_config
from flask_sqlalchemy import SQLAlchemy
from flask_api import status
from backend.flaskr import QUESTIONS_PER_PAGE, create_app
from backend.models import setup_db, Question, Category
from integration_db import create_test_dataset, remove_test_dataset, category_list, question_list

QUESTIONS_PER_CATEGORY = 10


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = create_app(".env.test")
        self.client = self.app.test_client

        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # creates the fake data
            remove_test_dataset(self.db)
            create_test_dataset(self.db)

    def setUp(self):
        """Executed before each test runs"""

    def tearDown(self):
        """Executed after each test runs"""
        pass

    @classmethod
    def tearDownClass(self):
        """Executed after the test suite runs"""
        pass

    # TODO [X] GET /api/v1.0/categories should get a list of categories
    def test_get_categories_should_return_200(self):
        """Test should get the list of categories  """
        url = '/api/v1.0/categories'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['data']), len(category_list))
        self.assertEqual(data['success'], True)

    # TODO [X] GET /api/v1.0/<ENDPOINT> should return 404 if not exists
    def test_get_wrong_url_should_return_404(self):
        """Test should return 404 if the url is mistyped """
        url = '/api/v1.0/categorie'
        res = self.client().get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # TODO [X] GET /api/v1.0/questions/ should return all questions paginated
    def test_get_questions(self):
        """Test should return all the question paginated """
        url = '/api/v1.0/questions'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True),
        self.assertEqual(data['total'], len(question_list))
        self.assertEqual(data['page'], 1),
        self.assertEqual(
            data['pages'],
            math.ceil(
                len(question_list) /
                QUESTIONS_PER_PAGE)),
        self.assertEqual(data['perPage'], QUESTIONS_PER_PAGE)

    # TODO [X] GET /api/v1.0/questions?page=3 should return the 3rd page of
    # questions
    def test_get_questions_page(self):
        """Test should return all the question for the specified page """
        pagenumber = 3
        url = f'/api/v1.0/questions?page={pagenumber}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True),
        self.assertEqual(data['total'], len(question_list))
        self.assertEqual(data['page'], pagenumber),
        self.assertEqual(
            data['pages'],
            math.ceil(
                len(question_list) /
                QUESTIONS_PER_PAGE)),
        self.assertEqual(data['perPage'], QUESTIONS_PER_PAGE)

    # TODO [X] GET /api/v1.0/questions?page=300 should return 404 if not exists
    def test_get_questions_page_not_exists(self):
        """Test should return 404 if the specified page does not exists"""
        pagenumber = 300
        url = f'/api/v1.0/questions?page={pagenumber}'
        res = self.client().get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

     # TODO [X] /api/v1.0/questions?perPage=3 should return the 3 items

    # TODO [X] GET /api/v1.0/questions?perpage=3 should return 3 items
    def test_get_questions_items_perpage(self):
        """Test should return all the question for the specified page """
        perpage = 3
        url = f'/api/v1.0/questions?perPage={perpage}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True),
        self.assertEqual(data['total'], len(question_list))
        self.assertEqual(data['page'], 1),
        self.assertEqual(
            data['pages'], math.ceil(
                len(question_list) / perpage)),
        self.assertEqual(data['perPage'], perpage)
        self.assertEqual(len(data['data']), perpage),

    # TODO [X] GET /api/v1.0/questions?category=2 should return all items for
    # category 2
    def test_get_questions_category(self):
        """Test should return all the question for the specified page """
        category = 2
        url = f'/api/v1.0/questions?category={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True),
        self.assertEqual(data['total'], 10)
        self.assertEqual(data['page'], 1),
        self.assertEqual(data['pages'], math.ceil(10 / QUESTIONS_PER_PAGE)),
        self.assertEqual(data['perPage'], QUESTIONS_PER_PAGE)

    # TODO [X] GET /api/v1.0/questions?category=200 should return 422
    def test_get_questions_category_not_exists(self):
        """Test should return Unprocessable """
        category = -1
        url = f'/api/v1.0/questions?category={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False),

    # TODO [X] GET /api/v1.0/questions/category?id=1 should return 200
    def test_get_all_questions_by_category_id(self):
        """Test should return 200 and the list of questions """
        category = 1
        url = f'/api/v1.0/questions/category?id={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(data['category']['id'], category)

    # TODO [X] GET /api/v1.0/questions/category?type=crafts should return 200
    def test_get_all_questions_by_category_type(self):
        """Test should return 200 and the list of questions """
        category = 'crafts'
        url = f'/api/v1.0/questions/category?type={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(data['category']['type'], category)

    # TODO [X] GET /api/v1.0/questions/category should return 422
    def test_get_all_questions_by_category_type_none(self):
        """Test should return 422"""
        category = None
        url = f'/api/v1.0/questions/category?type={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    # TODO [X] GET /api/v1.0/questions/category should return 422

    def test_get_all_questions_by_category_type_both(self):
        """Test should return 422 """
        url = f'/api/v1.0/questions/category?type=science&id=3'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    # TODO [X] GET /api/v1.0/questions/category should return 422
    def test_get_all_questions_by_category_id_none(self):
        """Test should return 422 """
        category = None
        url = f'/api/v1.0/questions/category?id={category}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    # TODO [X] POST RAND /api/v1.0/questions/random should return 200
    def test_get_random_question(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/random'
        res = self.client().post(url, json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['available'], len(question_list) - 1)
        self.assertIsInstance(data['data'], dict)
        self.assertIsNone(data['category'])
        self.assertIn(data['data']['id'], data['previous'])

    # TODO [X] POST RAND /api/v1.0/questions/random with category  should
    # return 200
    def test_get_random_question_with_category(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/random'
        category = 2
        res = self.client().post(url, json={'category': category})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['available'], QUESTIONS_PER_CATEGORY - 1)
        self.assertIsInstance(data['data'], dict)
        self.assertIsInstance(data['category'], dict)
        self.assertEqual(data['category']['id'], category)
        self.assertIn(data['data']['id'], data['previous'])

    # TODO [X] POST RAND /api/v1.0/questions/random with previous should
    # return 200
    def test_get_random_question_with_previous(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/random'
        _json = {
            'previous': [22, 17]
        }
        res = self.client().post(url, json=_json)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['available'], len(
            question_list) - (len(_json['previous']) + 1))
        self.assertIsInstance(data['data'], dict)
        self.assertIsNone(data['category'])
        self.assertEqual(len(data['previous']), 3)
        self.assertIn(data['data']['id'], data['previous'])

    # TODO [X] POST RAND /api/v1.0/questions/random with bad category should
    # return 422
    def test_get_random_question_with_bad_category(self):
        """Test should return 422 """
        url = f'/api/v1.0/questions/random'
        category = 2254
        res = self.client().post(url, json={'category': category})
        self.assertEqual(res.status_code, 422)

    # TODO [X] POST RAND /api/v1.0/questions/random with invalid previous ids
    # should return 200
    def test_get_random_question_with_bad_previous(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/random'
        _json = {
            'previous': [22, 17, 666]
        }
        res = self.client().post(url, json=_json)
        data = json.loads(res.data)
        expected_len = (len(_json['previous']))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data['data'], dict)
        self.assertIsNone(data['category'])
        # The api disregards bad previous ids so the available should return
        # the actual count
        self.assertEqual(data['available'], len(question_list) - expected_len)
        # Invalid ids are not removed from the list at the moment
        self.assertEqual(len(data['previous']), expected_len + 1)
        self.assertIn(data['data']['id'], data['previous'])

    # TODO [X] DEL /api/v1.0/questions/666 should return 404 not found
    def test_delete_question_not_exists(self):
        """Test should return Not found """
        id = 666
        url = f'/api/v1.0/questions/{id}'
        res = self.client().delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # TODO [X] DEL /api/v1.0/questions/<int> should return 200 after
    # successful deletion
    def test_delete_question(self):
        """Test should return 200 """
        question = Question(
            question='question 666',
            answer='answer 666',
            category=1,
            difficulty=5)
        id = None
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.session.add(question)
            self.db.session.commit()
            id = question.id

        url = f'/api/v1.0/questions/{id}'
        res = self.client().delete(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # TODO [X] POST NEW /api/v1.0/questions should return 200 after successful
    # submission
    def test_add_question(self):
        url = f'/api/v1.0/questions'
        _json = {
            'question': 'Another question',
            'answer': '42',
            'category': 2,
            'difficulty': 1
        }

        res = self.client().post(url, json=_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data['data'], dict)

        # Clean up
        id = data['data']['id']
        url = f'/api/v1.0/questions/{id}'
        res = self.client().delete(url)

    # TODO [X] POST NEW /api/v1.0/questions should return 422 if category not
    # valid
    def test_add_question_invalid_category(self):
        url = f'/api/v1.0/questions'
        _json = {
            'question': 'Another question',
            'answer': '42',
            'category': 27642,
            'difficulty': 1
        }
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 422)

    # TODO [ ] POST NEW /api/v1.0/questions should return 422 if difficulty
    # not valid
    def test_add_question_invalid_difficulty(self):
        url = f'/api/v1.0/questions'
        _json = {
            'question': 'Another question',
            'answer': '42',
            'category': 1,
            'difficulty': 0
        }
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 422)

    # TODO [ ] POST NEW /api/v1.0/questions should return 422 if difficulty
    # not valid
    def test_add_question_missing_difficulty(self):
        url = f'/api/v1.0/questions'
        _json = {
            'question': 'Another question',
            'answer': '42',
            'category': 1
        }
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 422)

    # TODO [ ] POST NEW /api/v1.0/questions should return 422 if question or
    # answer are null or empty
    def test_add_question_invalid_QandA(self):
        url = f'/api/v1.0/questions'
        _json = {
            'question': '',
            'answer': '',
            'category': 2,
            'difficulty': 1
        }
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 422)

    # TODO [ ] POST NEW /api/v1.0/questions should return 500 if internal
    # error occurs
    def test_add_question_internal_error(self):
        url = f'/api/v1.0/questions'
        _json = 'question'
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 500)

    # TODO [X] POST FIND /api/v1.0/questions/search should return 200 after
    # successful submission
    def test_search_questions(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/search'
        _json = {'search': 'est'}
        res = self.client().post(url, json=_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), len(question_list))
        self.assertEqual(data['found'], len(question_list))

    # TODO [X] POST FIND /api/v1.0/questions/search should return 200 if
    # search is empty
    def test_search_questions_empty_string(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/search'
        _json = {
            'search': '  '
        }
        res = self.client().post(url, json=_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(data['found'], 0)

    # TODO [X] POST FIND /api/v1.0/questions/search should return 200 if
    # search is empty
    def test_search_questions_nothing_found(self):
        """Test should return 200 """
        url = f'/api/v1.0/questions/search'
        _json = {
            'search': 'udacity'
        }
        res = self.client().post(url, json=_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(data['found'], 0)

    # TODO [X] POST FIND /api/v1.0/questions/search should return 422 if
    # search not valid
    def test_search_questions_no_query(self):
        """Test should return 422 """
        url = f'/api/v1.0/questions/search'
        _json = {'zearch': 'XYZ'}
        res = self.client().post(url, json=_json)
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
