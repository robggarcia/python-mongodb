from flask import Flask, redirect, url_for, request, session
from flask_cors import CORS, cross_origin
import json
from bson import ObjectId
from typing import Any
import bcrypt


from db import db


app = Flask(__name__)
app.secret_key = "poptarts"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

names_col = db.get_collection('names_col')
books_col = db.get_collection("books")
users_col = db.get_collection("users")

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


@app.route("/books/<book_id>", methods=['PATCH'])
def update_book(book_id):
    print(f"Update Book: {book_id}")
    to_update = request.get_json()
    print(to_update)
    try:
        updated = books_col.update_one(
            {"_id": ObjectId(book_id)}, {"$set": to_update})
        print(updated.modified_count)
        if updated.modified_count > 0:
            return {"success": True, "message": "Book successfully updated"}
        else:
            return {"success": False, "message": "Unable to update book"}, 404
    except:
        return {"success": False, "message": "Invalid book id"}, 500


@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


@app.route("/user/register", methods=["POST"])
def register():
    message = ''
    if "email" in session:
        # return redirect(url_for("logged_in"))
        return "User already logged in"
    if request.method == "POST":
        user = request.get_json()["username"]
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        user_found = users_col.find_one({"username": user})
        email_found = users_col.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that username'
            return {"success": True, "message": message}
        if email_found:
            message = 'This email already exists in database'
            return {"success": False, "message": message}
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_input = {'username': user, 'email': email, 'password': hashed}
            users_col.insert_one(user_input)

            user_data = users_col.find_one({"email": email})
            new_email = user_data['email']

            return {"success": True, "message": f"New User created with email: {new_email}"}
    return "User Register route working"


@app.route("/user/login", methods=["POST"])
def login():
    messsage = 'Please login to your account'
    if "email" in session:
        # return redirect(url_for("logged_in"))
        return "User already logged in"
    if request.method == "POST":
        email = request.get_json()["email"]
        password = request.get_json()["password"]

        email_found = users_col.find_one({"email": email})
        if email_found:
            email_val = email_found["email"]
            passwordcheck = email_found["password"]

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return {"success": True, "message": f"User logged in with email: {email_val}"}
            else:
                if "email" in session:
                    return "already logged in"
                message = 'Wrong password'
                return {"success": False, "message": message}
        else:
            message = 'Email not found'
            return {"success": False, "message": message}
    return {"success": False, "message": message}


if __name__ == "__main__":
    app.run(host='localhost', port=3500, debug=True)
