# from bson.objectid import ObjectId
# from pymongo import MongoClient
# import os
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import json
from user_api import user_api  # Import the user_api module

app = Flask(__name__)
app.register_blueprint(user_api, url_prefix='/api')

def get_database():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(os.getenv("MONGODB_URI"))

    # Create the database for our example (we will use the same database throughout the tutorial)
    return client["users"]


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()
    app.run(debug=True)
    print(dbname)
