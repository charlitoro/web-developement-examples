import os
import flask
from flask import request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from src.models import Book



@app.route('/', methods=['GET'])
def init():
    return "Hello World!!"


@app.route('/api/books/all', methods=['GET'])
def api_all():
    books = db.session.query(Book).filter().all()
    result = []
    for book in books:
        result.append(book.serialize())
    return jsonify(result)


@app.route('/api/book', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Empty list for our results
    results = []

    books = db.session.query(Book).filter(Book.id==id)
    for book in books:
        results.append(book.serialize())

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/update/book', methods=['POST'])
def api_update_book():
    # Check if an ID was provided as part of the URL.
    # If no ID is provided, display an error in the browser.
    body = request.get_json()
    if 'id' not in body:
        return "Error: No id field provided. Please specify an id."
    
    name = body.get("name")
    author = body.get("author")
    published = body.get("published")

    # Loop through the data and match results that fit the requested ID.
    found_book = db.session.query(Book).filter(Book.id==body.get("id")).first()
    if found_book is not None:
        if name is not None:
            found_book.name = name
        if author is not None:
            found_book.author = author
        if published is not None:
            found_book.published = published
    else:
        return "Error: Book not found"

    db.session.add(found_book)
    db.session.commit()
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(found_book.serialize())


@app.route('/api/create/book', methods=['POST'])
def create_book():
    data = request.get_json()

    name = data.get("name")
    author = data.get("author")
    published = data.get("published")

    book = Book(
        name=name,
        author=author,
        published=published
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.serialize())

app.run()