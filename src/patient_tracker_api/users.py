"""users.py
users module for functions that help with getting
and setting users 
"""
from __future__ import annotations  # for annotating class methods
from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto

# import collection from pymongo
import pymongo


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


def get_user(collection, username: str) -> dict:
    """gets user from database

    Parameters
    ----------
    collection :
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
        users = collection.find({"_id": username})
        print(users[0].get("id"))
        return users[0]
    except TypeError as e:
        """if something internal went wrong in the code"""
        return e, 500
    except Exception as e:
        return e, 404


def create_user(db, user: dict) -> str:
    """creates user in database

    Parameters
    ----------
    db :
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
