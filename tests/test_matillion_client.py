import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import HTTPError

from pymatillion.constants import (
    BASE_URL,
    PASSWORD,
    PROJECT_GROUP_NAME,
    PROJECT_NAME,
    USERNAME,
)
from pymatillion.matillion import MatillionClient

DUMMY_URL = "https://fakematillioninstance.com"
DUMMY_USERNAME = "fake_user"
DUMMY_PASSWORD = "fake_pass"
DUMMY_PROJECT_GROUP_NAME = "Sample_Project_Group"
DUMMY_PROJECT_NAME = "Sample_Project_1"
DUMMY_JOB_NAME = "Sample_Job_1"
DUMMY_TASK_ID = 12345


PARENT_DIR = Path(__file__).parent


class TestMatillionClient(TestCase):
    client: MatillionClient

    def setUp(self):
        self.client = MatillionClient(DUMMY_URL, DUMMY_USERNAME, DUMMY_PASSWORD)

    def test_attributes(self):
        self.client.project_name = DUMMY_PROJECT_NAME
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME

        self.assertEqual(self.client.base_url, DUMMY_URL)
        self.assertEqual(self.client.username, DUMMY_USERNAME)
        self.assertEqual(self.client.password, DUMMY_PASSWORD)
        self.assertEqual(self.client.project_group_name, DUMMY_PROJECT_GROUP_NAME)
        self.assertEqual(self.client.project_name, DUMMY_PROJECT_NAME)

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_project_groups(self, mock_get, mock_ensure_attributes):
        with open(PARENT_DIR.joinpath("list_project_groups_response.json")) as response:
            json_content = json.load(response)
        mock_get.return_value.json.return_value = json_content
        project_groups = self.client.list_project_groups()
        self.assertListEqual(project_groups, json_content)
        mock_ensure_attributes.called_once_with(BASE_URL, USERNAME, PASSWORD)

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_project_group_without_url(self, mock_get, mock_ensure_attributes):
        self.client.base_url = ""
        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {BASE_URL}")
        ]
        with self.assertRaises(ValueError) as cm:
            self.client.list_project_groups()
        self.assertEqual(f"Undefined attributes: {BASE_URL}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(BASE_URL, USERNAME, PASSWORD)
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_project_group_without_username(
        self, mock_get, mock_ensure_attributes
    ):
        self.client.username = ""
        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {USERNAME}")
        ]
        with self.assertRaises(ValueError) as cm:
            self.client.list_project_groups()
        self.assertEqual(f"Undefined attributes: {USERNAME}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(BASE_URL, USERNAME, PASSWORD)
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_project_group_without_password(
        self, mock_get, mock_ensure_attributes
    ):
        self.client.password = ""
        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {PASSWORD}")
        ]
        with self.assertRaises(ValueError) as cm:
            self.client.list_project_groups()
        self.assertEqual(f"Undefined attributes: {PASSWORD}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(BASE_URL, USERNAME, PASSWORD)
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.requests.get")
    def test_list_project_groups_when_attributes_unauthorized(self, mock_get):
        self.client.password = "xyz"
        self.client.username = "abc"

        with open(PARENT_DIR.joinpath("unauthorized_response.json")) as response:
            json_content = json.load(response)
        mock_get.side_effect = HTTPError(json_content["msg"])

        with self.assertRaises(HTTPError) as cm:
            self.client.list_project_groups()

        self.assertEqual(json_content["msg"], cm.exception.args[0])

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_projects(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME

        with open(PARENT_DIR.joinpath("list_projects_response.json")) as response:
            json_content = json.load(response)
        mock_get.return_value.json.return_value = json_content

        projects = self.client.list_projects()

        self.assertListEqual(projects, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME
        )

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_projects_without_url(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.base_url = ""

        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {BASE_URL}")
        ]

        with self.assertRaises(ValueError) as cm:
            self.client.list_projects()

        self.assertEqual(f"Undefined attributes: {BASE_URL}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME
        )
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_projects_without_password(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.password = ""

        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {PASSWORD}")
        ]

        with self.assertRaises(ValueError) as cm:
            self.client.list_projects()

        self.assertEqual(f"Undefined attributes: {PASSWORD}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME
        )
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.requests.get")
    def test_list_projects_when_attributes_unauthorized(self, mock_get):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME

        self.client.password = "xyz"
        self.client.username = "abc"

        with open(PARENT_DIR.joinpath("unauthorized_response.json")) as response:
            json_content = json.load(response)
        mock_get.side_effect = HTTPError(json_content["msg"])

        with self.assertRaises(HTTPError) as cm:
            self.client.list_projects()

        self.assertEqual(json_content["msg"], cm.exception.args[0])

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_jobs(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        with open(PARENT_DIR.joinpath("list_jobs_response.json")) as response:
            json_content = json.load(response)
        mock_get.return_value.json.return_value = json_content

        jobs = self.client.list_jobs()

        self.assertListEqual(jobs, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_jobs_without_url(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME
        self.client.base_url = ""

        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {BASE_URL}")
        ]

        with self.assertRaises(ValueError) as cm:
            self.client.list_jobs()

        self.assertEqual(f"Undefined attributes: {BASE_URL}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_list_jobs_without_password(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME
        self.client.password = ""

        mock_ensure_attributes.side_effect = [
            ValueError(f"Undefined attributes: {PASSWORD}")
        ]

        with self.assertRaises(ValueError) as cm:
            self.client.list_jobs()

        self.assertEqual(f"Undefined attributes: {PASSWORD}", cm.exception.args[0])
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        mock_get.assert_not_called()

    @patch("pymatillion.matillion.requests.get")
    def test_list_jobs_when_attributes_unauthorized(self, mock_get):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        self.client.password = "xyz"
        self.client.username = "abc"

        with open(PARENT_DIR.joinpath("unauthorized_response.json")) as response:
            json_content = json.load(response)
        mock_get.side_effect = HTTPError(json_content["msg"])

        with self.assertRaises(HTTPError) as cm:
            self.client.list_jobs()

        self.assertEqual(json_content["msg"], cm.exception.args[0])

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.post")
    def test_run_job(self, mock_post, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        with open(PARENT_DIR.joinpath("run_job_response.json")) as response:
            json_content = json.load(response)
        mock_post.return_value.json.return_value = json_content

        run_job_response = self.client.run_job(job_name=DUMMY_JOB_NAME)

        self.assertEqual(run_job_response, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.get")
    def test_get_task_details(self, mock_get, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        with open(PARENT_DIR.joinpath("task_detail_response.json")) as response:
            json_content = json.load(response)
        mock_get.return_value.json.return_value = json_content

        task_detail_response = self.client.get_task_details(task_id=DUMMY_TASK_ID)

        self.assertEqual(task_detail_response, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.post")
    def test_delete_project(self, mock_post, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        with open(PARENT_DIR.joinpath("delete_project_response.json")) as response:
            json_content = json.load(response)
        mock_post.return_value.json.return_value = json_content

        delete_project_response = self.client.delete_project(
            project_name=DUMMY_PROJECT_NAME
        )

        self.assertEqual(delete_project_response, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )

    @patch("pymatillion.matillion.MatillionClient._ensure_attributes")
    @patch("pymatillion.matillion.requests.post")
    def test_delete_job(self, mock_post, mock_ensure_attributes):
        self.client.project_group_name = DUMMY_PROJECT_GROUP_NAME
        self.client.project_name = DUMMY_PROJECT_NAME

        with open(PARENT_DIR.joinpath("delete_job_response.json")) as response:
            json_content = json.load(response)
        mock_post.return_value.json.return_value = json_content

        delete_job_response = self.client.delete_job(job_name=DUMMY_JOB_NAME)

        self.assertEqual(delete_job_response, json_content)
        mock_ensure_attributes.called_once_with(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
