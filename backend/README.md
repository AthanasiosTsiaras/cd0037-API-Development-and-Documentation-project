# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

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

used Postgres.app for local development.

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

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


## API Reference

### Getting Started
* **Base URL:** Currently, this app can only be run locally. The backend is hosted at `http://127.0.0.1:5000/`.
* **Authentication:** This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API will return five types of errors for various failure conditions:
* **400:** Bad Request
* **404:** Resource Not Found
* **405:** Method Not Allowed
* **422:** Unprocessable
* **500:** Internal Server Error

---

### Endpoints

#### `GET /categories`
- **General:** Fetches a dictionary of categories where keys are the IDs and values are the category names.
- **Request Arguments:** None
- **Returns:** An object with `categories` and `success` status.
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### `GET /questions`
- **General:** Returns a list of questions, number of total questions, current category, and categories.
- **Request Arguments:** `page` (optional integer, defaults to 1).
- **Returns:** Paginated questions (10 per page).
```json
{
  "categories": { "1": "Science", "2": "Art" },
  "current_category": null,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of Greece?",
      "answer": "Athens",
      "category": "3",
      "difficulty": 1
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### `DELETE /questions/<int:question_id>`
- **General:** Deletes a question of a given ID if it exists.
- **Request Arguments:** `question_id` (Path parameter).
- **Returns:** ID of the deleted question and success status.
```json
{
  "deleted": 1,
  "success": true
}
```

#### `POST /questions`
- **General:** This endpoint handles two distinct actions:
    1. **Create:** If no `searchTerm` is provided, it creates a new question.
    2. **Search:** If a `searchTerm` is provided, it returns questions containing that string.
- **Request Body (Create):** `question` (str), `answer` (str), `difficulty` (int), `category` (str).
- **Request Body (Search):** `searchTerm` (str).
- **Returns (Create):** ID of created question.
- **Returns (Search):** List of matching questions.
```json
{
  "questions": [],
  "success": true,
  "total_questions": 10
}
```

#### `GET /categories/<int:category_id>/questions`
- **General:** Returns all questions belonging to a specific category.
- **Request Arguments:** `category_id` (Path parameter).
- **Returns:** Paginated questions within that category.
```json
{
  "questions": [...],
  "total_questions": 5,
  "current_category": "Science",
  "success": true
}
```

#### `POST /quizzes`
- **General:** Returns a single random question within a chosen category that has not been previously asked.
- **Request Body:** `previous_questions` (list of IDs), `quiz_category` (object with `id` and `type`).
- **Returns:** A single question object.
```json
{
  "question": {
    "id": 5,
    "question": "How many states are in the US?",
    "answer": "50",
    "category": "3",
    "difficulty": 1
  },
  "success": true
}
```

---

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
