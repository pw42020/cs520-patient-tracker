"""users.py
users module for functions that help with getting
and setting users 
"""
import pymongo
from dataclasses import dataclass


@dataclass
class User:
    """functional interface to represent a user"""

    ...


def get_user(db: pymongo.database.Database, username: str) -> dict:
    """gets user from database

    Parameters
    ----------
    db : pymongo.database.Database
        database to grab user from
    username : str
        username of user to grab

    Returns
    -------
    dict
        user if successful

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        print("hello world")
        collection = db[username]
        print(collection.find_all())
        print("fortnite")
        user = collection.find_one()
        return user
    except Exception as e:
        return e, 404
