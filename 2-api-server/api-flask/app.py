import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def init():
    return "Hello World!!"


@app.route('/api/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/books', methods=['GET'])
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
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(found_book)

app.run()