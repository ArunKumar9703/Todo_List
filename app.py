from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# ---- MongoDB connection (same URI you use in Compass) ----
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
todo_collection = db["todo_items"]


@app.route("/")
def todo_page():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json(silent=True) or request.form
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"message": "itemName and itemDescription are required"}), 400

    result = todo_collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })
    return jsonify({
        "message": "Item saved successfully",
        "id": str(result.inserted_id)
    })

if __name__ == "__main__":
    app.run(debug=True)