"""main app for patient tracker api"""
import json
from typing import Final
from pathlib import Path

from flask import Flask

from patient_tracker_api import users, db

ROOT_PATH: Final[Path] = Path(__file__).parent.parent

# defining app
app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    """initialization to ensure that app is running
    and database can be grabbed

    Returns
    -------
    str
        ping if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    return db.ping_database()


@app.route("/users/<username>")
def get_user(username: str) -> dict:
    """gets user from database

    Parameters
    ----------
    username : str
        username of user to grab

    Returns
    -------
    dict
        user if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    users_db = db.get_database("users")
    print("username: " + username)
    try:
        return users.get_user(users_db, username)
    except Exception:
        return f"user {username} not found", 404


@app.route("/create_user/<user_data>")
def create_user(user_data: str) -> str:
    """creates user in database

    Parameters
    ----------
    user_data : str
        user_data of user to create

    Returns
    -------
    str
        user's id if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    users_db = db.get_database("users")
    try:
        return users.create_user(users_db, user_data)
    except Exception:
        return f"user {user_data.get('_id')} not created", 403
