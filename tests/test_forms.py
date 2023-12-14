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
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
PATH_TO_ROOT: Path = Path(__file__).parent.parent
PATH_TO_APP: Path = PATH_TO_ROOT / "src"
sys.path.append(str(PATH_TO_APP))

DATETIME_TO_ADD: str = "2023-12-13T12:26:43Z"

from app import app

removeIds = []


class TestFormsAPI(unittest.TestCase):
    """testing module for testing patient_tracker_api module
    through specifically the Flask interface"""

    def setUp(self) -> None:
        """initialization for testing"""
        self.app = app.test_client()
        logging.basicConfig(stream=sys.stderr)

    def test_create_form(self) -> None:
        """tests create_form function in app.py"""
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

        with open(f"{PATH_TO_ROOT}/assets/default_form.json", "r") as f:
            form_json = json.loads(f.read())

        form_json.update({"patient_id": patient_json.get("_id")})

        form_json.update({"_id": str(uuid.uuid4())})
        self.assertEqual(
            self.app.post(
                "/create_form",
                data=json.dumps(form_json),
                content_type="application/json",
            ).status_code,
            http.HTTPStatus.OK,
        )



    def test_get_form(self) -> None:
        """test ability to get specific created form"""

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


        return_val = self.app.post(
            f"/create_form",
            data=json.dumps(
                {
                    "patient_id": patient_json["_id"],
                    "diagnosis": "anonymous_diagnosis",
                }
            ),
            content_type="application/json",
        )
        
        

        self.assertEqual(
            return_val.status_code,
            http.HTTPStatus.OK,
        )

        # test get appointment for
        self.assertEqual(
            self.app.get(f"/{patient_json['_id']}/forms").status_code,
            http.HTTPStatus.OK,
        )




if __name__ == "__main__":
    unittest.main()
