from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os

user_api = Blueprint('user_api', __name__)

# MongoDB Atlas connection string
client = MongoClient(os.getenv("MONGODB_URI"))

# Connect to your database
db = client["users"] 


@user_api.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Extract user data from the request
        user_data = request.json
        username = user_data.get('username')

        # Check if username already exists
        users_collection = db.users  # Replace 'users' with your collection name
        if users_collection.find_one({'username': username}):
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

        # Insert new user data into the MongoDB collection
        result = users_collection.insert_one(user_data)

        # Return a success response
        return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

