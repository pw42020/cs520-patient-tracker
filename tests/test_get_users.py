"""testing module for testing patient_tracker_api module
through specifically the Flask interface"""
import sys
import http
import json
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


class TestGetUsers(unittest.TestCase):
    def setUp(self) -> None:
        """initialization for testing"""
        self.app = app.test_client()

    def test_sign_in(self) -> None:
        """testing sign-in function after creating a user"""

        with open(f"{PATH_TO_ROOT}/assets/default_doctor.json", "r") as f:
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
            self.app.post(
                f"/sign_in",
                data=json.dumps(
                    {
                        "username": user_json["_id"],
                        "password": user_json["password"],
                    }
                ),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

    def test_get_user(self) -> None:
        """tests get_user function in app.py"""

        with open(f"{PATH_TO_ROOT}/assets/default_doctor.json", "r") as f:
            doctor_json = json.loads(f.read())

        with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
            patient_json = json.loads(f.read())

        doctor_json.update(
            {"_id": str(uuid.uuid4())}
        )  # random username to not conflict
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(doctor_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        # create patient
        patient_json.update(
            {"_id": str(uuid.uuid4())}
        )  # random username to not conflict
        self.assertEqual(
            self.app.post(
                f"/create_user",
                data=json.dumps(patient_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.post(
                f"/users/{patient_json.get('_id')}",
                data=json.dumps({"caller_id": doctor_json.get("_id")}),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )

        self.assertEqual(
            self.app.post(
                f"/users/{doctor_json.get('_id')}",
                data=json.dumps({"caller_id": patient_json.get("_id")}),
                content_type="application/json",
            ).status_code,
            404,
        )

        # self.assertEqual(
        #     self.app.get(f"/users/foobar").status_code,
        #     http.HTTPStatus.NOT_FOUND,
        # )

    # removeIds.append(user_json["_id"])


if __name__ == "__main__":
    unittest.main()
