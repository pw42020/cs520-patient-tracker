"""testing module for testing patient_tracker_api module
through specifically the Flask interface"""
import sys
import http
import json
import logging
import unittest
import uuid
from pathlib import Path

# required to get all code in src/ folder
PATH_TO_ROOT: Path = Path(__file__).parent.parent
PATH_TO_APP: Path = PATH_TO_ROOT / "src"
sys.path.append(str(PATH_TO_APP))

from app import app


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
            user_data = json.loads(f.read())

        user_data.update({"_id": str(uuid.uuid4())})  # random username to not conflict
        logging.warning(
            self.app.post(
                "/create_user",
                data=str(user_data),
            )
        )
        # self.assertEqual(
        #     self.app.post(
        #         "/create_user",
        #         data=user_data,
        #     ).status_code,
        #     http.HTTPStatus.OK,
        # )

    # def test_get_user(self) -> None:
    #     """tests get_user function in app.py"""

    #     with open(f"{PATH_TO_ROOT}/assets/default_patient.json", "r") as f:
    #         user_data = json.loads(f.read())

    #     user_id: str = str(uuid.uuid4())

    #     user_data.update({"_id": user_id})  # random username to not conflict
    #     self.assertEqual(
    #         self.app.post(
    #             "/create_user",
    #             data=user_data,
    #         ).status_code,
    #         http.HTTPStatus.OK,
    #     )

    #     self.assertEqual(
    #         self.app.get(f"/users/{user_id}").status_code,
    #         http.HTTPStatus.NOT_FOUND,
    #     )


if __name__ == "__main__":
    unittest.main()
