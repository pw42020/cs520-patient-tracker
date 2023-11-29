from flask import Flask

from patient_tracker_api import users, db

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
    return users.get_user(users_db, username)
