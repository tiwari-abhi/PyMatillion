import json
from unittest import TestCase
from unittest.mock import patch

from pathlib import Path

from requests.exceptions import HTTPError

from pymatillion.matillion import MatillionClient
from pymatillion.constants import BASE_URL, USERNAME, PASSWORD

DUMMY_URL = 'https://fakematillioninstance.com'
DUMMY_USERNAME = 'fake_user'
DUMMY_PASSWORD = 'fake_pass'
DUMMY_PROJECT_GROUP_NAME = 'Sample_Project_Group'
DUMMY_PROJECT_NAME = 'Sample_Project_1'


PARENT_DIR = Path(__file__).parent

class TestMatillionClient(TestCase):

    def setUp(self):
        self.client = MatillionClient(DUMMY_URL, DUMMY_USERNAME, DUMMY_PASSWORD)

    def test_attributes(self):
        client = MatillionClient(
            DUMMY_URL, DUMMY_USERNAME, DUMMY_PASSWORD, DUMMY_PROJECT_GROUP_NAME, DUMMY_PROJECT_NAME
        )
        self.assertEqual(client.base_url, DUMMY_URL)
        self.assertEqual(client.username, DUMMY_USERNAME)
        self.assertEqual(client.password, DUMMY_PASSWORD)
        self.assertEqual(client.project_group_name, DUMMY_PROJECT_GROUP_NAME)
        self.assertEqual(client.project_name, DUMMY_PROJECT_NAME)

    @patch('pymatillion.matillion.requests.get')
    @patch('pymatillion.matillion.MatillionClient._ensure_attributes')
    def test_list_project_groups(self, mock_ensure_attributes, mock_get):
        with open(PARENT_DIR.joinpath('list_project_groups_response.json')) as response:
            json_content = json.load(response)
        mock_get.return_value.json.return_value = json_content
        project_groups = self.client.list_project_groups()
        self.assertListEqual(project_groups, json_content)
        mock_ensure_attributes.assert_called_once_with(BASE_URL, USERNAME, PASSWORD)

    @patch('pymatillion.matillion.requests.get')
    def test_list_project_group_without_url(self, mock_get):
        client = MatillionClient(
            base_url='', username=DUMMY_USERNAME, password=DUMMY_PASSWORD
        )
        with self.assertRaises(ValueError) as cm:
            client.list_project_groups()
        self.assertEqual(f'Undefined attributes: {BASE_URL}', cm.exception.args[0])
        mock_get.assert_not_called()

    @patch('pymatillion.matillion.requests.get')
    def test_list_project_group_without_username(self, mock_get):
        client = MatillionClient(
            base_url=DUMMY_URL, username='', password=DUMMY_PASSWORD
        )
        with self.assertRaises(ValueError) as cm:
            client.list_project_groups()
        self.assertEqual(f'Undefined attributes: {USERNAME}', cm.exception.args[0])
        mock_get.assert_not_called()

    @patch('pymatillion.matillion.requests.get')
    def test_list_project_group_without_password(self, mock_get):
        client = MatillionClient(
            base_url=DUMMY_URL, username=DUMMY_USERNAME, password=''
        )
        with self.assertRaises(ValueError) as cm:
            client.list_project_groups()
        self.assertEqual(f'Undefined attributes: {PASSWORD}', cm.exception.args[0])
        mock_get.assert_not_called()

    @patch('pymatillion.matillion.requests.get')
    def test_list_project_when_attributes_unauthorized(self, mock_get):
        bad_pass_client = MatillionClient(
            base_url=DUMMY_URL, username=DUMMY_USERNAME, password='abc'
        )
        bad_user_client = MatillionClient(
            base_url=DUMMY_URL, username='abc', password=DUMMY_PASSWORD
        )

        with open(PARENT_DIR.joinpath('unauthorized_response.json')) as response:
            json_content = json.load(response)
        mock_get.side_effect = HTTPError(json_content['msg'])

        with self.assertRaises(HTTPError) as cm_bp:
            bad_pass_client.list_project_groups()

        with self.assertRaises(HTTPError) as cm_bu:
            bad_user_client.list_project_groups()

        self.assertNotEquals(bad_pass_client.password, DUMMY_PASSWORD)
        self.assertNotEquals(bad_user_client.username, DUMMY_USERNAME)

        self.assertEqual(json_content['msg'], cm_bp.exception.args[0])
        self.assertEqual(json_content['msg'], cm_bu.exception.args[0])