from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# helper function for paginated queries
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # .format() as defined in models.py
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        # convert categories to dict
        categories_dict = {category.id: category.type for category in categories}

        if len(categories_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions')
    def get_questions():
        # query questions and categories
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        
        # paginate questions
        current_questions = paginate_questions(request, selection)

        # dict formatting
        categories_dict = {category.id: category.type for category in categories}

        # check empty
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict,
            'current_category': None  # Default 'All'
        })
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # query question by id
            question = Question.query.filter(Question.id == question_id).one_or_none()

            # check empty response
            if question is None:
                abort(404)

            # delete
            question.delete()

            # response
            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            # 
            abort(422)

    # FE uses /questions for both search and create. need to combine as below.
    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():
        body = request.get_json()
        
        # if searchTerm exists else None
        search_term = body.get('searchTerm', None)

        if search_term:
            try:
                # query questions with search_term
                selection = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')
                ).all()

                # paginate
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                    'current_category': None
                })

            except Exception:
                abort(422)

        # otherwise create
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            # create body qc
            if not (new_question and new_answer and new_difficulty and new_category):
                abort(422)

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'total_questions': len(Question.query.all())
                })

            except Exception:
                abort(422)
    
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # query category by id
        category = Category.query.filter(Category.id == category_id).one_or_none()
        
        # check if exists
        if category is None:
            abort(404)

        try:
            # query questions by category id
            selection = Question.query.filter(Question.category == str(category_id)).all()
            
            # paginate
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category.type
            })

        except Exception:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            # parse request body
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            # 2. Start building the query
            if category['id'] == 0:
                # if not category id then query all questions
                selection = Question.query.all()
            else:
                # query questions based on category id
                selection = Question.query.filter(Question.category == str(category['id'])).all()

            # filter out previously asked questions
            available_questions = [q for q in selection if q.id not in previous_questions]

            # if available_questions not empty pick random
            new_question = None
            if len(available_questions) > 0:
                new_question = random.choice(available_questions).format()

            # 5. Return the single question
            return jsonify({
                'success': True,
                'question': new_question
            })

        except Exception:
            abort(422)

    # error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

