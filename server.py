from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

try:
    client = MongoClient("mongodb+srv://kavishka:kav1234@cluster0.ddfkm.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('test-db')
    newRow = db.book_details

except:
    print("Database not connected.")


@app.route('/api/books', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        try:
            details = request.json
            book_id = details["id"]
            title = details["title"]
            edition = details["edition"]
            author = details["author"]
            description = details["description"]
            category = details["category"]

            book_dict = {"id": book_id, "title": title, "edition": edition, "author": author,
                         "description": description, "category": category}
            newRow.insert_one(book_dict)

            return jsonify("Book added successfully")
        except Exception:
            return jsonify("Error")
    if request.method == 'GET':

        category = request.args.get('category')
        if category:
            data = []
            for doc in newRow.find({"category": category}):
                doc['_id'] = str(doc['_id'])
                data.append(doc)
            if not data:
                return jsonify("Not Found")
            else:
                return jsonify(data)
        else:
            data = []
            for doc in newRow.find({}):
                doc['_id'] = str(doc['_id'])
                data.append(doc)

            if not data:
                return jsonify("Not Found")
            else:
                return jsonify(data)


@app.route('/api/books/<book_id>', methods=['PUT'])
def edit_book(book_id):
    data = newRow.find_one({"id": book_id})
    if data:
        newRow.update_one({'id': book_id}, {"$set": request.json}, upsert=False)
        return jsonify("Book update successfully")
    else:
        return jsonify("Not Found")


@app.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    data = newRow.find_one({"id": book_id})
    if data:
        newRow.delete_one({'id': book_id})
        return jsonify("Book deleted successfully")
    else:
        return jsonify("Not Found")


@app.route('/api/books/<book_id>', methods=['GET'])
def view_book(book_id):
    book = newRow.find_one({"id": book_id})
    if book:
        book_id = book["id"]
        title = book["title"]
        edition = book["edition"]
        author = book["author"]
        description = book["description"]
        category = book["category"]

        book_dict = {"id": book_id, "title": title, "edition": edition, "author": author,
                     "description": description, "category": category}
        return jsonify(book_dict)
    else:
        return jsonify("Not Found")

if __name__ == "__main__":
    app.run(debug=True)
