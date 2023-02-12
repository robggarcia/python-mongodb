from flask import Flask, redirect, url_for, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json
from bson import ObjectId
from typing import Any

from db import db

MONGODB_URI = 'mongodb+srv://yoshi:test123@cluster0.tvnuyyw.mongodb.net/?retryWrites=true&w=majority'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

names_col = db.get_collection('names_col')
books_col = db.get_collection("books")

# create a bson encoder to handle Mongo Cursors


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        # if isinstance(o, datetime):
        #     return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/addname/<name>/')
def addname(name):
    names_col.insert_one({"name": name.lower()})
    return redirect(url_for('getnames'))


@app.route('/getnames/')
def getnames():
    names_json = []
    if names_col.find({}):
        for name in names_col.find({}).sort("name"):
            names_json.append({"name": name['name'], "id": str(name['_id'])})
    # return json.dumps(names_json)
    return names_json


@app.route("/books")
def getbooks():
    # books_json = [{"title": book['title'], "id": str(book["_id"])}
    #   for book in books_col.find({}).sort("author")]
    # if books_col.find({}):
    #     for book in books_col.find({}).sort("author"):
    #         books_json.append({"book": book['author']})
    # return json.dumps(books, default=str)
    books = books_col.find({}).sort("author")
    books_json = MongoJSONEncoder().encode(list(books))
    books_obj = json.loads(books_json)
    return books_obj


@app.route("/books", methods=['POST'])
def create_book():
    # new_book = json.loads(request.data)
    new_book = request.get_json()
    # print(type(new_book))
    response = books_col.insert_one(new_book)
    print(str(response.inserted_id))

    if response.inserted_id != None:
        new_item = books_col.find({"_id": ObjectId(response.inserted_id)})
        books_json = MongoJSONEncoder().encode(list(new_item))
        books_obj = json.loads(books_json)
        return books_obj
    else:
        return ({"success": False, "message": "Unable to create book"})

    # # Prepare the response
    # if isinstance(response, list):
    #     # Return list of Id of the newly created item
    #     return jsonify([str(v) for v in response]), 201
    # else:
    #     # Return Id of the newly created item
    #     return jsonify(str(response)), 201
    # # return jsonify(str(response))


@app.route("/books/<book_id>", methods=["DELETE"])
def remove_book(book_id):
    print(f"Delete book: {book_id}")
    try:
        delete_book = books_col.delete_one({"_id": ObjectId(book_id)})
        print(delete_book.deleted_count)
        if delete_book.deleted_count > 0:
            return {"success": True, "message": "Book successfully deleted"}
        else:
            return {"success": False, "message": "Unable to delete book"}, 404
    except:
        return {"success": False, "message": "Invalid book id"}, 500


@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


if __name__ == "__main__":
    app.run(host='localhost', port=3500, debug=True)
