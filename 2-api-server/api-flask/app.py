import flask
from flask import request, jsonify

# local imports
from src.data import books

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def init():
    return "Hello World!!"


@app.route('/api/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


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

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

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
    
    title = body.get("title")
    author = body.get("author")
    published = body.get("published")

    # Loop through the data and match results that fit the requested ID.
    found_book = None
    for book in books:
        if book['id'] == body["id"]:
            found_book = book
            break
    if found_book is not None:
        if title is not None:
            found_book["title"] = title
        if author is not None:
            found_book["author"] = author
        if published is not None:
            found_book["published"] = published
    else:
        return "Error: Book not found"
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(found_book)

app.run()