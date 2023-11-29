"""Appointments file that contains the class for appointments, 
and the functions to create, get, and delete appointments
"""
from __future__ import annotations  # for annotating class methods
from dataclasses import dataclass
import uuid

import pymongo


@dataclass
class Appointment:
    id: str
    doctor_id: str
    patient_id: str
    date: str
    summary: str

    @classmethod
    def from_json(cls, data: dict) -> Appointment:
        """converts json to appointment

        Parameters
        ----------
        data : dict
            json representation of appointment

        Returns
        -------
        Appointment
            appointment if successful

        Notes
        -----
        Takes case if there is an ID, otherwise creates a new one using uuid.uuid4()
        """
        if data.get("_id"):
            return cls(
                id=data.get("_id"),
                doctor_id=data.get("doctor_id"),
                patient_id=data.get("patient_id"),
                date=data.get("date"),
                summary=data.get("summary"),
            )
        else:
            return cls(
                id=uuid.uuid4(),
                doctor_id=data.get("doctor_id"),
                patient_id=data.get("patient_id"),
                date=data.get("date"),
                summary=data.get("summary"),
            )

    def to_json(self) -> dict:
        """converts appointment to json

        Returns
        -------
        dict
            json representation of appointment
        """
        return {
            "_id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "date": self.date,
            "summary": self.summary,
        }


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
        appointments_db.insert_one(appointment.to_json())
        return appointment.id
    except Exception as e:
        return e, 500
