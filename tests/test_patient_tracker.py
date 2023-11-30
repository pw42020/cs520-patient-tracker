"""testing module for testing patient_tracker_api module
through specifically the Flask interface"""
import sys
import http
import json
import logging
import unittest
import uuid
from pathlib import Path
from datetime import datetime

# required to get all code in src/ folder
DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"
PATH_TO_ROOT: Path = Path(__file__).parent.parent
PATH_TO_APP: Path = PATH_TO_ROOT / "src"
sys.path.append(str(PATH_TO_APP))

from app import app

removeIds = []


class TestPatientTrackerAPI(unittest.TestCase):
    """testing module for testing patient_tracker_api module
    through specifically the Flask interface"""

    def setUp(self) -> None:
        """initialization for testing"""
        self.app = app.test_client()
        logging.basicConfig(stream=sys.stderr)

    def test_ping_db(self) -> None:
        """tests ping_db function in app.py"""
        self.assertEqual(
            self.app.get("/").status_code,
            http.HTTPStatus.OK,
        )

    def test_create_user(self) -> None:
        """tests create_user function in app.py"""
        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            user_json = json.loads(f.read())

        user_json.update({"_id": str(uuid.uuid4())})  # random username to not conflict
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(user_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        removeIds.append(user_json["_id"])

    def test_delete_user(self) -> None:
        """tests delete_user function in app.py"""
        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            user_json = json.loads(f.read())

        user_json.update({"_id": str(uuid.uuid4())})  # random username to not conflict
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(user_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.delete(
                f"/delete_user/{user_json['_id']}",
                data=json.dumps({"password": user_json["password"]}),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        # testing that user is no longer gettable in database

    def test_get_user(self) -> None:
        """tests get_user function in app.py"""

        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            user_json = json.loads(f.read())

        user_json.update({"_id": str(uuid.uuid4())})  # random username to not conflict
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(user_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.get(f"/users/{user_json.get('_id')}").status_code,
            http.HTTPStatus.OK,
        )

        removeIds.append(user_json["_id"])

    def test_update_user(self) -> None:
        """tests update_user function in app.py"""

        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            user_json = json.loads(f.read())

        user_json.update({"_id": str(uuid.uuid4())})
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(user_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.put(
                f"/update_user/{user_json['_id']}",
                data=json.dumps(
                    {
                        "password": user_json["password"],
                        "update_param": {"name": "test"},
                    }
                ),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        removeIds.append(user_json["_id"])

    def test_create_appointment(self) -> None:
        """tests create_appointment function in app.py"""
        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            patient_json = json.loads(f.read())

        patient_json.update({"_id": str(uuid.uuid4())})
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(patient_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        with open(f"{PATH_TO_ROOT}/assets/default_doctor.json", "r") as f:
            doctor_json = json.loads(f.read())

        doctor_json.update({"_id": str(uuid.uuid4())})
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(doctor_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.post(
                f"/create_appointment",
                data=json.dumps(
                    {
                        "doctor_id": doctor_json["_id"],
                        "patient_id": patient_json["_id"],
                        "date": datetime.now().strftime(DATETIME_FORMAT),
                        "summary": "test",
                    }
                ),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )


if __name__ == "__main__":
    unittest.main()
