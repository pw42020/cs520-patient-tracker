"""main app for patient tracker api"""
import sys
import json
import hashlib
from typing import Final
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask import request  # for multiple param input like with appointments

from pymongo.database import Database

from patient_tracker_api import forms, users, db, appointments
from patient_tracker_api.users import DoctorPatient

ROOT_PATH: Final[Path] = Path(__file__).parent.parent

sys.path.append(f"{str(ROOT_PATH)}/assets")  # to add logging formatter
from CustomFormatter import CustomFormatter


# defining app
def create_app():
    return Flask(__name__)


app = create_app()
CORS(app)


@app.route("/", methods=["GET"])
def ping_db() -> str:
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


@app.route("/users/<username>", methods=["POST"])
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

    caller_id: str = request.get_json().get("caller_id")
    users_db = db.get_database("users")

    if caller_id is None:
        return "invalid input", 400

    user, status_code = users.get_user(users_db, caller_id)

    if status_code != 200:
        return "something went wrong with user", status_code

    if user.doctorPatient == 1:
        return f"User {username} not found", 404

    user, status_code = users.get_user(users_db, username)
    user_json: dict[str, str] = user.to_json()
    # remove sensitive information
    user_json.pop("password")
    user_json.pop("SSN")
    try:
        return user_json, status_code
    except Exception:
        return f"user {username} not found", 404


@app.route("/sign_in", methods=["POST"])
def sign_in() -> dict:
    """sign in a user with a username and password"""
    user_password = request.get_json()
    users_db = db.get_database("users")
    user, status_code = users.get_user(users_db, user_password.get("username"))
    if status_code != 200:
        return user, status_code
    if (
        hashlib.sha256(user_password.get("password").encode()).hexdigest()
        != user.password
    ):
        return "invalid password", 400
    if status_code != 200:
        return "something went wrong with user", status_code
    return user.to_json(), 200


@app.route("/create_user", methods=["POST"])
def create_user() -> str:
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

    user_data = request.get_json()

    try:
        return users.create_user(users_db, user_data)
    except Exception:
        return f"user {user_data.get('_id')} not created", 403


@app.route("/update_user/<user_id>", methods=["PUT"])
def update_user(user_id: str) -> int:
    """updates user in database

    Parameters
    ----------
    user_id : str
        id of user to update
    update_param : str
        parameter to update

    Returns
    -------
    int
        status code if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    users_db = db.get_database("users")

    update_param = request.json.get("update_param")
    password = request.json.get("password")
    try:
        # turn update_param into dict through json
        return user_id, users.update_user(users_db, user_id, password, update_param)
    except Exception:
        return f"user {user_id} not updated", 403


@app.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id: str) -> int:
    """deletes user in database"""

    user_password = request.get_json().get("password")

    users_db = db.get_database("users")
    try:
        return users.delete_user(users_db, user_id, user_password)
    except Exception:
        return f"user {user_id} not deleted", 403


@app.route("/create_appointment", methods=["POST"])
def create_appointment():
    """creates appointment in database

    Parameters
    ----------
    appointment_data : str
        appointment_data of appointment to create

    Returns
    -------
    str
        appointment's id if successful

    Raises
    ------
    Exception
        if unsuccessful"""

    appointment_data = request.get_json()
    if (
        appointment_data.get("doctor_id") is None
        or appointment_data.get("patient_id") is None
        or appointment_data.get("date") is None
        or appointment_data.get("summary") is None
    ):
        return "invalid input", 400

    appointment = appointments.Appointment.from_json(appointment_data)

    appointments_db = db.get_database("appointments")
    users_db = db.get_database("users")

    try:
        # update user and doctor appointmentIds
        doctor, status_code = users.get_user(users_db, appointment.doctor_id)
        if status_code != 200:
            raise Exception("doctor not found")
        doctor.appointmentIds.append(appointment.id)
        users.update_user(
            db=users_db,
            user_id=appointment.doctor_id,
            password=None,
            update_param={"appointmentIds": doctor.appointmentIds},
        )

        patient, status_code = users.get_user(users_db, appointment.patient_id)
        if status_code != 200:
            raise Exception("patient not found")
        patient.appointmentIds.append(appointment.id)
        users.update_user(
            db=users_db,
            user_id=appointment.patient_id,
            password=None,
            update_param={"appointmentIds": patient.appointmentIds},
        )

        appointments.create_appointment(appointments_db, appointment)
        return appointment.id, 200
    except Exception as e:
        return e, 500


@app.route("/appointments/<appointment_id>", methods=["GET"])
def get_appointment(appointment_id: str) -> dict:
    """gets appointment from database

    Parameters
    ----------
    appointment_id : str
        id of appointment to get from database

    Returns
    -------
    dict
        appointment if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    appointments_db = db.get_database("appointments")
    appointment = appointments.get_appointment(appointments_db, appointment_id)
    try:
        return appointment.to_json(), 200
    except Exception:
        return f"appointment {appointment_id} not found", 404


@app.route("/<username>/appointments", methods=["GET"])
def get_appointments(username: str) -> dict:
    """Get all appointments for user

    Parameters
    ----------
    username : str
        username of user to get appointments for

    Returns
    -------
    dict
        appointments if successful
    """
    user_db: Database = db.get_database("users")
    appointments_db: Database = db.get_database("appointments")

    user, status_code = users.get_user(user_db, username)
    if status_code != 200:
        return "something went wrong with user", status_code

    appointments_dict: dict = {}
    for appointment_id in user.appointmentIds:
        appointment: appointments.Appointment = appointments.get_appointment(
            appointments_db, appointment_id
        )
        appointments_dict.update({appointment_id: appointment.to_json()})

    return appointments_dict


# Creating form


@app.route("/create_form", methods=["POST"])
def create_form():
    """creates form in database

    Parameters
    ----------
    form_data : str
        form_data of form to create

    Returns
    -------
    str
        form's id if successful

    Raises
    ------
    Exception
        if unsuccessful"""

    form_data = request.get_json()
    if (
        form_data.get("referringDoctorId") is None
        or form_data.get("patientId") is None
        or form_data.get("diagnosis") is None
    ):
        return "invalid input", 400

    form = forms.form.from_json(form_data)

    forms_db = db.get_database("forms")
    users_db = db.get_database("users")

    try:
        # update user and doctor formIds
        doctor, status_code = users.get_user(users_db, form.referringDoctorId)
        if status_code != 200:
            raise Exception("doctor not found")
        doctor.formIds.append(form.id)
        users.update_user(
            db=users_db,
            user_id=form.referringDoctorId,
            password=None,
            update_param={"formIds": doctor.formIds},
        )

        patient, status_code = users.get_user(users_db, form.patient_id)
        if status_code != 200:
            raise Exception("patient not found")
        patient.formIds.append(form.id)
        users.update_user(
            db=users_db,
            user_id=form.patient_id,
            password=None,
            update_param={"formIds": patient.formIds},
        )

        forms.create_form(forms_db, form)
        return form.id, 200
    except Exception as e:
        return e, 500


@app.route("/forms/<form_id>", methods=["GET"])
def get_form(form_id: str) -> dict:
    """gets form from database

    Parameters
    ----------
    form_id : str
        id of form to get from database

    Returns
    -------
    dict
        form if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    forms_db = db.get_database("forms")
    form = forms.get_form(forms_db, form_id)
    try:
        return form.to_json(), 200
    except Exception:
        return f"form {form_id} not found", 404


@app.route("/<username>/forms", methods=["GET"])
def get_forms(username: str) -> dict:
    """Get all forms for user

    Parameters
    ----------
    username : str
        username of user to get forms for

    Returns
    -------
    dict
        forms if successful
    """
    user_db: Database = db.get_database("users")
    forms_db: Database = db.get_database("forms")

    user, status_code = users.get_user(user_db, username)
    if status_code != 200:
        return "something went wrong with user", status_code

    forms_dict: dict = {}
    for form_id in user.formIds:
        form: forms.form = forms.get_form(forms_db, form_id)
        forms_dict.update({form_id: form.to_json()})

    return forms_dict


@app.route("/<name>/search", methods=["GET"])
def search_users(name: str) -> dict:
    """Get all forms for user

    Parameters
    ----------
    username : str
        username of user to get forms for

    Returns
    -------
    dict
        forms if successful
    """
    user_db: Database = db.get_database("users")
    user, status_code = users.get_profile(user_db, name)
    if status_code != 200:
        return "something went wrong with user", status_code

    return user


@app.route("/<name>/doctors", methods=["GET"])
def search_doctors(name: str) -> dict:
    """Get all forms for user

    Parameters
    ----------
    username : str
        username of user to get forms for

    Returns
    -------
    dict
        forms if successful
    """
    user_db: Database = db.get_database("users")
    user, status_code = users.get_doctors(user_db, name)
    if status_code != 200:
        return "something went wrong with user", status_code

    return user


# defining app

if __name__ == "__main__":
    # add default_patient.json to database
    with open(f"{ROOT_PATH}/assets/default_doctor.json", "r") as f:
        user_json = json.loads(f.read())

    users_db = db.get_database("users")
    users.create_user(users_db, user_json)
