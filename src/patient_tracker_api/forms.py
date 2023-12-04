"""forms.py form file that contains the class for form, 
and the functions to create, get, and delete form
"""
from __future__ import annotations  # for annotating class methods
import sys
from dataclasses import dataclass
import uuid

import pymongo



@dataclass
class form:
    id: str
    patient_id: str
    patientName: str
    patientDOB: str
    referringDoctor: str
    referringDoctorId: str
    referringDoctorPhone: str
    briefClinicalHistory: str
    diagnosis: str
    studyDate: str
    pdfUrl: list[str]

    @classmethod
    def from_json(cls, data: dict) -> form:
        """converts json to form

        Parameters
        ----------
        data : dict
            json representation of form

        Returns
        -------
        form
            form if successful

        Notes
        -----
        Takes case if there is an ID, otherwise creates a new one using uuid.uuid4()
        """
        if data.get("_id"):
            return cls(
                id=data.get("_id"),
                patient_id=data.get("patient_id"),
                patientName=data.get("patientName"),
                patientDOB=data.get("patientDOB"),
                referringDoctor=data.get("referringDoctor"),
                referringDoctorId=data.get("referringDoctorId"),
                referringDoctorPhone=data.get("referringDoctorPhone"),
                briefClinicalHistory=data.get("briefClinicalHistory"),
                diagnosis=data.get("diagnosis"),
                studyDate=data.get("studyDate"),
                pdfUrl=data.get("pdfUrl"),
                
            )
        else:
            return cls(
                id=str(uuid.uuid4()),
                patient_id=data.get("patient_id"),
                patientName=data.get("patientName"),
                patientDOB=data.get("patientDOB"),
                referringDoctor=data.get("referringDoctor"),
                referringDoctorId=data.get("referringDoctorId"),
                referringDoctorPhone=data.get("referringDoctorPhone"),
                briefClinicalHistory=data.get("briefClinicalHistory"),
                diagnosis=data.get("diagnosis"),
                studyDate=data.get("studyDate"),
                pdfUrl=data.get("pdfUrl"),
            )

    def to_json(self) -> dict:
        """converts form to json

        Returns
        -------
        dict
            json representation of form
        """
        return {
            "_id": self.id,
            "patient_id": self.patient_id,
            "patientName": self.patientName,
            "patientDOB": self.patientDOB,
            "referringDoctor": self.referringDoctor,
            "referringDoctorId": self.referringDoctorId,
            "referringDoctorPhone": self.referringDoctorPhone,
            "briefClinicalHistory": self.briefClinicalHistory,
            "diagnosis": self.diagnosis,
            "studyDate": self.studyDate,
            "pdfUrl": self.pdfUrl,
        }


def create_form(
    form_db: pymongo.databases.database, form: form
) -> str:
    """creates form in database

    Parameters
    ----------
    form_db : pymongo.databases.database
        database to add form to
    form : form
        form to add to database

    Returns
    -------
    str
        id of form if successful

    Raises
    ------
    Exception
        if unsuccessful
    """
    try:
        # add to form database
        form_db.insert_one(form.to_json())
        return form.id
    except Exception as e:
        print(e, file=sys.stderr)
        return e, 500


def get_form(
    form_db: pymongo.databases.database, form_id: str
) -> form | None:
    """gets form from database

    Parameters
    ----------
    form_db : pymongo.databases.database
        database to get form from
    form_id : str
        id of form to get from database

    Returns
    -------
    tuple[form, int]
        form if successful with status code

    Raises
    ------
    Exception
        if unsuccessful
    """
    form_json = form_db.find_one({"_id": form_id})

    return form.from_json(form_json) if form_json else None
