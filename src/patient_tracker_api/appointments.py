"""Appointments file that contains the class for appointments, 
and the functions to create, get, and delete appointments
"""
from __future__ import annotations  # for annotating class methods
import sys
from dataclasses import dataclass
import uuid

import pymongo


@dataclass
class Appointment:
    """functional interface to represent an appointment""

    Attributes
    ----------
    _id : str
        id of appointment
    doctor_id : str
        id of doctor
    patient_id : str
        id of patient
    date : str
        date of appointment
    summary : str
        summary of appointment
    """

    _id: str = str(uuid.uuid4())
    doctor_id: str
    patient_id: str
    date: str
    summary: str


def create_appointment(
    appointments_db: pymongo.databases.database, appointment: Appointment
) -> str:
    """creates appointment in database

    Parameters
    ----------
    appointments_db : pymongo.databases.database
        database to add appointment to
    appointment : Appointment
        appointment to add to database

    Returns
    -------
    str
        id of appointment if successful

    Raises
    ------
    Exception
        if unsuccessful
    """
    try:
        # add to appointments database
        appointments_db.insert_one(appointment.to_json())
        return appointment.id
    except Exception as e:
        print(e, file=sys.stderr)
        return e, 500


def get_appointment(
    appointments_db: pymongo.databases.database, appointment_id: str
) -> Appointment | None:
    """gets appointment from database

    Parameters
    ----------
    appointments_db : pymongo.databases.database
        database to get appointment from
    appointment_id : str
        id of appointment to get from database

    Returns
    -------
    tuple[Appointment, int]
        appointment if successful with status code

    Raises
    ------
    Exception
        if unsuccessful
    """
    appointment_json = appointments_db.find_one({"_id": appointment_id})

    return Appointment(**appointment_json) if appointment_json else None
