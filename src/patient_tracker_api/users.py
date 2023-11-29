"""users.py
users module for functions that help with getting
and setting users 
"""
from __future__ import annotations  # for annotating class methods
from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto

# import database from pymongo
from pymongo.database import Database


class DoctorPatient(Enum):
    """enum to represent whether user is a doctor or patient"""

    doctor = auto()
    patient = auto()


@dataclass
class User:
    """functional interface to represent a user"""

    id: str
    doctorPatient: Enum
    name: str
    DOB: str
    password: str
    SSN: str
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

    @classmethod
    def from_json(cls, data: dict) -> User:
        """converts json to user

        Parameters
        ----------
        data : dict
            json representation of user

        Returns
        -------
        User
            user if successful
        """
        return cls(
            id=data.get("_id"),
            doctorPatient=data.get("doctorPatient"),
            name=data.get("name"),
            DOB=data.get("DOB"),
            password=data.get("password"),
            SSN=data.get("SSN"),
            formIds=data.get("formIds"),
            gender=data.get("gender"),
            address1=data.get("address1"),
            address2=data.get("address2"),
            city=data.get("city"),
            state=data.get("state"),
            zip=data.get("zip"),
            imageUrl=data.get("imageUrl"),
            appointmentIds=data.get("appointmentIds"),
            availableSlots=data.get("availableSlots"),
        )

    def to_json(self) -> dict:
        """converts user to json

        Returns
        -------
        dict
            json representation of user"""
        json: dict = {}
        json["_id"] = self.id
        json["doctorPatient"] = self.doctorPatient
        json["name"] = self.name
        json["DOB"] = self.DOB
        json["password"] = self.password
        json["SSN"] = self.SSN
        json["formIds"] = self.formIds
        json["gender"] = self.gender
        json["address1"] = self.address1
        json["address2"] = self.address2
        json["city"] = self.city
        json["state"] = self.state
        json["zip"] = self.zip
        json["imageUrl"] = self.imageUrl
        json["appointmentIds"] = self.appointmentIds
        json["availableSlots"] = self.availableSlots

        return json


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
        user = db.find_one({"_id": username})
        if user is None:
            return f"user {username} not found", 404
        else:
            user = User.from_json(user)
            return user, 200
    except TypeError as e:
        """if something internal went wrong in the code"""
        return e, 500
    except Exception as e:
        return e, 404


def create_user(db: Database, user: dict) -> str:
    """creates user in database

    Parameters
    ----------
    db: Database
        database to create user in
    user : User
        user to create

    Returns
    -------
    str
        user's id if successful

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        db.insert_one(user)
        return user.get("_id")
    except Exception as e:
        return e, 500


def update_user(db: Database, user_id: str, update_param: dict) -> int:
    """updates the user in the database

    Parameters
    ----------
    db : Database
        database to update user in
    user_id : str
        id of user to update
    update_param : dict
        json representation of user to update

    Returns
    -------
    int
        0 if successful, 1 if not
    """
    db.update_one({"_id": user_id}, {"$set": update_param})


def delete_user(db: Database, user_id: str, password: str) -> tuple[str, int]:
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
    tuple[str, int]
        tuple containing the id of the user deleted and the status code

    Notes
    -----
    password is required so the user can only be deleted by the actual
    user themself, not by anyone else.
    """
    try:
        db.delete_one({"_id": user_id})
        return user_id, 200
    except Exception as e:
        return e, 500
