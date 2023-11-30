"""main app for patient tracker api"""
import sys
import logging
import json
from typing import Final, Any
from pathlib import Path

from flask import Flask
from flask import request  # for multiple param input like with appointments

from pymongo.database import Database

from patient_tracker_api import users, db, appointments

ROOT_PATH: Final[Path] = Path(__file__).parent.parent

sys.path.append(f"{str(ROOT_PATH)}/assets")  # to add logging formatter
from CustomFormatter import CustomFormatter


# defining app
def create_app():
    return Flask(__name__)


app = create_app()


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


@app.route("/users/<username>", methods=["GET"])
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
    user, status_code = users.get_user(users_db, username)
    try:
        return user.to_json(), status_code
    except Exception:
        return f"user {username} not found", 404


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
        print(e, file=sys.stderr)
        return e, 500


"""DEPRECATED"""
# @app.route("/user_exists/<username>", methods=["GET"])
# def user_exists(username: str) -> bool:
#     """checks if user exists in database

#     Parameters
#     ----------
#     username : str
#         username of user to check

#     Returns
#     -------
#     bool
#         if user exists or not"""
#     users_db = db.get_database("users")
#     try:
#         user, status_code = users.get_user(users_db, username)
#         return user.get("_id") == None, status_code
#     except Exception:
#         return False, 500


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


if __name__ == "__main__":
    app.run(debug=True)
