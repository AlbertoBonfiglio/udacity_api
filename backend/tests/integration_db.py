from flask_sqlalchemy import SQLAlchemy

from backend.models import Category, Question

category_list: [] = [  # type: ignore
    Category(type='arts'),
    Category(type='crafts'),
    Category(type='beers'),
    Category(type='drunken people')
]

question_list: [] = [  # type: ignore
    Question(
        question='question 0',
        answer='answer 0',
        category=0,
        difficulty=1),
    Question(
        question='question 1',
        answer='answer 1',
        category=0,
        difficulty=2),
    Question(
        question='question 2',
        answer='answer 2',
        category=0,
        difficulty=3),
    Question(
        question='question 3',
        answer='answer 3',
        category=0,
        difficulty=4),
    Question(
        question='question 3',
        answer='answer 4',
        category=0,
        difficulty=5),
    Question(
        question='question 5',
        answer='answer 5',
        category=1,
        difficulty=1),
    Question(
        question='question 6',
        answer='answer 6',
        category=1,
        difficulty=2),
    Question(
        question='question 7',
        answer='answer 7',
        category=1,
        difficulty=3),
    Question(
        question='question 8',
        answer='answer 8',
        category=1,
        difficulty=4),
    Question(
        question='question 9',
        answer='answer 9',
        category=1,
        difficulty=5),
    Question(
        question='question 10',
        answer='answer 10',
        category=0,
        difficulty=1),
    Question(
        question='question 11',
        answer='answer 11',
        category=0,
        difficulty=2),
    Question(
        question='question 12',
        answer='answer 12',
        category=0,
        difficulty=3),
    Question(
        question='question 13',
        answer='answer 13',
        category=0,
        difficulty=4),
    Question(
        question='question 14',
        answer='answer 14',
        category=0,
        difficulty=5),
    Question(
        question='question 15',
        answer='answer 15',
        category=1,
        difficulty=1),
    Question(
        question='question 16',
        answer='answer 16',
        category=1,
        difficulty=2),
    Question(
        question='question 17',
        answer='answer 17',
        category=1,
        difficulty=3),
    Question(
        question='question 18',
        answer='answer 18',
        category=1,
        difficulty=4),
    Question(
        question='question 19',
        answer='answer 19',
        category=1,
        difficulty=5),
    Question(
        question='question 20',
        answer='answer 20',
        category=0,
        difficulty=1),
    Question(
        question='question 21',
        answer='answer 21',
        category=0,
        difficulty=2),
    Question(
        question='question 22',
        answer='answer 22',
        category=0,
        difficulty=3),
    Question(
        question='question 23',
        answer='answer 23',
        category=0,
        difficulty=4),
    Question(
        question='question 24',
        answer='answer 24',
        category=0,
        difficulty=5),
    Question(
        question='question 25',
        answer='answer 25',
        category=1,
        difficulty=1),
    Question(
        question='question 26',
        answer='answer 26',
        category=1,
        difficulty=2),
    Question(
        question='question 27',
        answer='answer 27',
        category=1,
        difficulty=3),
    Question(
        question='question 28',
        answer='answer 28',
        category=1,
        difficulty=4),
    Question(
        question='question 29',
        answer='answer 29',
        category=1,
        difficulty=5),
    Question(
        question='question 30',
        answer='answer 30',
        category=0,
        difficulty=1),
    Question(
        question='question 31',
        answer='answer 31',
        category=0,
        difficulty=2),
    Question(
        question='question 32',
        answer='answer 32',
        category=0,
        difficulty=3),
    Question(
        question='question 33',
        answer='answer 33',
        category=0,
        difficulty=4),
    Question(
        question='question 34',
        answer='answer 34',
        category=0,
        difficulty=5),
    Question(
        question='question 35',
        answer='answer 35',
        category=1,
        difficulty=1),
    Question(
        question='question 36',
        answer='answer 36',
        category=1,
        difficulty=2),
    Question(
        question='question 37',
        answer='answer 37',
        category=1,
        difficulty=3),
    Question(
        question='question 38',
        answer='answer 38',
        category=1,
        difficulty=4),
    Question(
        question='question 39',
        answer='answer 39',
        category=1,
        difficulty=5),
]


def create_test_dataset(db: SQLAlchemy):
    idx = 0
    modulus = 10
    for category in category_list:
        db.session.add(category)
        db.session.commit()

        start = modulus * idx
        end = start + modulus
        qlist = question_list[start: end]
        for question in qlist:
            question.category = category.id
            db.session.add(question)

        idx += 1
    db.session.commit()


def remove_test_dataset(db: SQLAlchemy):
    db.session.query(Question).delete()
    db.session.query(Category).delete()

    # Resets the counters
    category_counter = 'ALTER SEQUENCE public."categories_id_seq" RESTART WITH 1'
    question_counter = 'ALTER SEQUENCE public."questions_id_seq" RESTART WITH 1'
    db.session.execute(question_counter)
    db.session.execute(category_counter)

    db.session.commit()
