"""users.py
users module for functions that help with getting
and setting users 
"""
from __future__ import annotations  # for annotating class methods
import sys
from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto
import hashlib


# import database from pymongo
from pymongo.database import Database


class DoctorPatient(Enum):
    """enum to represent whether user is a doctor or patient"""

    doctor = auto()
    patient = auto()


@dataclass
class User:
    """functional interface to represent a user"""

    _id: str
    doctorPatient: Enum
    name: str
    DOB: str
    password: bytes
    SSN: bytes
    formIds: list[str]
    gender: str
    address1: str
    address2: Optional[str]
    city: str
    state: str
    zip: str
    imageUrl: str
    appointmentIds: list[str]
    availableSlots: list[str]
    # optional option of public key for encryption, will simply send data
    # with warning that data is not encrypted if not provided for debugging
    publicKey: Optional[str] = None


def get_user(db: Database, username: str) -> tuple[User | str, int]:
    """gets user from database

    Parameters
    ----------
    db: Database
        database to grab user from
    username : str
        username of user to grab

    Returns
    -------
    tuple[User | str, int]
        user, status code if successful, error string and status code if not

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        user_json = db.find_one({"_id": username})
        if user_json is None:
            return f"user {username} not found", 404
        else:
            user = User(**user_json)
            return user, 200
    except TypeError as e:
        """if something internal went wrong in the code"""
        return e, 500
    except Exception as e:
        return e, 404


def get_profile(db: Database, name: str) -> tuple[list, int]:
    """gets user profile from database and return without the password field

    Parameters
    ----------
    db: Database
        database to grab user from
    name : str
        Name of user to grab

    Returns
    -------
    tuple[list(User | str), int]
        user, status code if successful, error string and status code if not

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        users: list[str] = db.find({"name": name}, {"password": 0})
        return list(users), 200
    except TypeError as e:
        """if something internal went wrong in the code"""
        return e, 500
    except Exception as e:
        return e, 404


def get_doctors(db: Database, name: str) -> tuple[list, int]:
    """gets docotor profile from database and return without the password and SSN field

    Parameters
    ----------
    db: Database
        database to grab user from
    name : str
        Name of user to grab

    Returns
    -------
    tuple[list(User | str), int]
        user, status code if successful, error string and status code if not

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        users: list[str] = db.find(
            {"name": name, "doctorPatient": 0}, {"password": 0, "SSN": 0}
        )
        return list(users), 200
    except TypeError as e:
        """if something internal went wrong in the code"""
        return e, 500
    except Exception as e:
        return e, 404


def create_user(db: Database, user: dict) -> tuple[str, int]:
    """creates user in database

    Parameters
    ----------
    db: Database
        database to create user in
    user : User
        user to create

    Returns
    -------
    tuple[str, int]
        user's id if successful with status code

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        possible_user: str = db.find_one({"_id": user.get("_id")})
        if possible_user is not None:
            return f"user {user.get('_id')} already exists", 403

        # hashing user's password and social security number
        user.update(
            {"password": hashlib.sha256(user.get("password").encode()).hexdigest()}
        )
        user.update({"SSN": hashlib.sha256(user.get("SSN").encode()).hexdigest()})

        db.insert_one(user)
        return user.get("_id"), 200
    except Exception as e:
        return e, 500


def update_user(db: Database, user_id: str, password: str, update_param: dict) -> int:
    """updates the user in the database

    Parameters
    ----------
    db : Database
        database to update user in
    user_id : str
        id of user to update
    password: str
        password of user to update, must have to update
    update_param : dict
        json representation of user to update

    Returns
    -------
    int
        0 if successful, 1 if not
    """

    user, status_code = get_user(db, user_id)
    if status_code != 200:
        return status_code

    # if user.password != password and update_param.keys()[0] != "appointmentIds":
    #     return 403
    db.update_one({"_id": user_id}, {"$set": update_param})


def delete_user(db: Database, user_id: str, password: str) -> int:
    """deletes the user in the database

    Parameters
    ----------
    db : Database
        database to delete user in
    user_id : str
        id of user to delete
    password: str
        password of user to delete

    Returns
    -------
    int
        status code

    Notes
    -----
    password is required so the user can only be deleted by the actual
    user themself, not by anyone else.
    """
    try:
        db.delete_one({"_id": user_id})
        return 200
    except Exception as e:
        print(e, file=sys.stderr)
        return 500


def update_user_encryption_key(users_db: Database, user_id: str, key: str) -> int:
    """updates the user's encryption key in the database

    Parameters
    ----------
    users_db : Database
        database to update user in
    user_id : str
        id of user to update
    key : str
        encryption key to update user with

    Returns
    -------
    int
        0 if successful, 1 if not
    """
    try:
        users_db.update_one({"_id": user_id}, {"$set": {"publicKey": key}})
        return 0
    except Exception as e:
        return 1


def get_public_key(users_db: Database, user_id: str) -> str:
    """gets the user's encryption key from the database

    Parameters
    ----------
    users_db : Database
        database to get user from
    user_id : str
        id of user to get

    Returns
    -------
    str
        encryption key if successful, empty string if not
    """
    try:
        user = users_db.find_one({"_id": user_id})
        return user.get("publicKey")
    except Exception as e:
        return ""
