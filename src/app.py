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
app = Flask(__name__)


@app.route("/")
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
    try:
        return users.get_user(users_db, username)
    except Exception:
        return f"user {username} not found", 404


@app.route("/create_user/<user_data>")
def create_user(user_data: str) -> str:
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
    try:
        return users.create_user(users_db, user_data)
    except Exception:
        return f"user {user_data.get('_id')} not created", 403


@app.route("/update_user/<user_id>/<update_param>")
def update_user(user_id: str, update_param: str) -> int:
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
    try:
        # turn update_param into dict through json
        update_param: dict[str, Any] = json.loads(update_param)
        return users.update_user(users_db, user_id, update_param)
    except Exception:
        return f"user {user_id} not updated", 403


@app.route("/create_appointment", methods=["GET"])
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

    doctor_id: str = request.args.get("doctor_id")
    patient_id: str = request.args.get("patient_id")
    date: str = request.args.get("date")
    summary: str = request.args.get("summary")

    if doctor_id is None or patient_id is None or date is None or summary is None:
        return "invalid input", 400

    appointment_data = {
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "date": date,
        "summary": summary,
    }

    appointment: appointments.Appointment = appointments.Appointment(appointment_data)

    appointments_db = db.get_database("appointments")
    try:
        return users.create_appointment(appointments_db, appointment)
    except Exception:
        return f"appointment {appointment.get('_id')} not created", 403


@app.route("/user_exists/<username>")
def user_exists(username: str) -> bool:
    """checks if user exists in database

    Parameters
    ----------
    username : str
        username of user to check

    Returns
    -------
    bool
        if user exists or not"""
    users_db = db.get_database("users")
    try:
        user, status_code = users.get_user(users_db, username)
        if status_code == 200 and user != None:
            return True
        else:
            return False
    except Exception:
        return False


@app.route("/get_appointments/<username>")
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

    user: users.User = users.get_user(user_db, username)

    appointments_dict: dict = {}
    for appointment_id in user.appointmentIds:
        appointment: appointments.Appointment = appointments.get_appointment(
            appointments_db, appointment_id
        )
        appointments_dict.update({appointment_id: appointment})

    return appointments_dict


if __name__ == "__main__":
    # format logger
    LOG_FORMAT = ["[%(asctime)s] [%(levelname)s]", "%(message)s "]

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    LOG_FILE = "patient_tracker_api.log"
    logger = logging.FileHandler(LOG_FILE)
    logger.setFormatter("".join(LOG_FORMAT))
    log.addHandler(logger)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    log.addHandler(ch)

    app.run(debug=True)
