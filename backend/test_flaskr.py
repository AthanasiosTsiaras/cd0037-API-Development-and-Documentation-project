import unittest
import json

from flaskr import create_app
from models import Question, Category, db

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        # Adjusted for Postgres.app (usually no password)
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', '', 'localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        })
        self.client = self.app.test_client

        # Bind the app to the current context
        with self.app.app_context():
            db.create_all()
            
            # Seed a category and question so tests have data to work with
            category = Category(type='Science')
            db.session.add(category)
            db.session.flush() # gets the ID
            
            question = Question(
                question='Test Question', 
                answer='Test Answer', 
                category=str(category.id), 
                difficulty=1
            )
            db.session.add(question)
            db.session.commit()
            
            self.test_question_id = question.id
            self.test_category_id = category.id

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            # respect foreign keys in drop order
            db.session.execute(db.text('DROP TABLE IF EXISTS questions CASCADE;'))
            db.session.execute(db.text('DROP TABLE IF EXISTS categories CASCADE;'))
            db.session.commit()

    # --- CATEGORY TESTS ---
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories_failure(self):
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # --- QUESTION TESTS ---
    def test_get_paginated_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'] > 0)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question_success(self):
        res = self.client().delete(f'/questions/{self.test_question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.test_question_id)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_question_success(self):
        new_q = {
            'question': 'New Test Question',
            'answer': 'Answer',
            'difficulty': 1,
            'category': str(self.test_category_id)
        }
        res = self.client().post('/questions', json=new_q)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # --- SEARCH TESTS ---
    def test_search_questions_success(self):
        res = self.client().post('/questions', json={'searchTerm': 'Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)

    # --- QUIZ TESTS ---
    def test_play_quiz_success(self):
        quiz_data = {
            'previous_questions': [],
            'quiz_category': {'type': 'Science', 'id': self.test_category_id}
        }
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

if __name__ == "__main__":
    unittest.main()