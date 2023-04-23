import logging
from typing import Dict, List

import requests

from pymatillion.constants import (
    API_GET,
    API_POST,
    BASE_URL,
    DEFAULT_VERSION,
    PASSWORD,
    PROJECT_GROUP_NAME,
    PROJECT_NAME,
    USERNAME,
)

logger = logging.getLogger(__name__)


class MatillionClient:
    def __init__(
        self, base_url, username, password, project_group_name=None, project_name=None
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.project_group_name = project_group_name
        self.project_name = project_name
        self._valid_attributes = False
        self._headers = None

    def _ensure_attributes(self, *args):
        attributes_to_check = set(args)
        invalid_attributes = []
        for attr in attributes_to_check:
            if (getattr(self, attr) is None) or (not getattr(self, attr)):
                invalid_attributes.append(attr)
        if invalid_attributes:
            raise ValueError(f'Undefined attributes: {",".join(invalid_attributes)}')
        else:
            self._valid_attributes = True

    def _set_headers(self):
        self._headers = {"Content-Type": "application/json"}

    def _api_request(
        self, http_method, *args, is_json=True, **kwargs
    ) -> requests.Response:
        """
        Make an API Request.

        Args:
            http_method (str) : HTTP method to use when making API request.
            args : Variable length list of strings to construct endpoint path.
            is_json (bool) : Set to False if payload/response is not JSON data.
            kwargs : Arbitrary keyword arguments to construct request payload.

        Returns:
            requests.Response : Response object.
        """

        api_request = getattr(requests, http_method)
        api_path = f'{self.base_url}/rest/v1/{"/".join(args)}'
        if is_json:
            if len(kwargs) == 1 and "json" in kwargs:
                response = api_request(
                    api_path,
                    headers=self._headers,
                    auth=(self.username, self.password),
                    json=kwargs["json"],
                )
            else:
                response = api_request(
                    api_path,
                    headers=self._headers,
                    auth=(self.username, self.password),
                    json=kwargs,
                )
        else:
            if len(kwargs) == 1 and "data" in kwargs:
                response = api_request(
                    api_path,
                    headers=self._headers,
                    auth=(self.username, self.password),
                    data=kwargs["data"],
                )
            else:
                response = api_request(
                    api_path,
                    headers=self._headers,
                    auth=(self.username, self.password),
                    data=kwargs,
                )
        try:
            response.raise_for_status()
        except Exception:
            logger.error(f"Response content:\n{response.content}")
            raise
        return response

    def list_project_groups(self) -> List[str]:
        """
        Retrieve Project Groups within the Matillion instance.

        Returns:
            Project Groups (list) : A list of strings with names of Project Groups.
        """
        self._ensure_attributes(BASE_URL, USERNAME, PASSWORD)
        return self._api_request(API_GET, "group").json()

    def list_projects(self) -> List[str]:
        """
        Retreive Projects within the specified Project Group of Matillion instance.

        Returns:
            Project Names (list) : A list of strings with names of Projects.
        """
        self._ensure_attributes(BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME)
        return self._api_request(
            API_GET, "group", "name", self.project_group_name, "project"
        ).json()

    def list_jobs(
        self, project_name: str = None, version: str = DEFAULT_VERSION
    ) -> List[str]:
        """
        Retrieve jobs within the specified version of the Matillion project.

        Args:
            project_name (str): Name of the Matillion project.
            version: (str), optional. Default value : default.
        Returns:
            Matillion Jobs (list): A list of of strings with names of the Matillion jobs.
        """
        self._ensure_attributes(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        return self._api_request(
            API_GET,
            "group",
            "name",
            self.project_group_name,
            "project",
            "name",
            project_name if project_name else self.project_name,
            "version",
            "name",
            version,
            "job",
        ).json()

    def run_job(
        self,
        job_name: str,
        job_variables: dict = {},
        grid_variables: dict = {},
        project_name: str = None,
        version: str = DEFAULT_VERSION,
    ) -> Dict:
        """
        Run Matillion job within the specified project, for the specified version.

        Args:
            job_name (str): Name of the Matillion job intended to run.
            job_variables (dict): Dictionary of Matillion job variables.
            grid_variables (dict): Dictionary of Matillion grid variables.
            project_name (str): Name of the Matillion project.
            version: (str), optional. Default value : default.
        Returns:
            dict : Sample response can be found at https://documentation.matillion.com/docs/2475544#server-response
        """
        self._ensure_attributes(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        body = {"scalarVariables": job_variables, "gridVariables": grid_variables}
        return self._api_request(
            API_POST,
            "group",
            "name",
            self.project_group_name,
            "project",
            "name",
            project_name if project_name else self.project_name,
            "version",
            "name",
            version,
            "job",
            "name",
            job_name,
            "run",
            json=body,
        ).json()

    def get_task_details(self, task_id: int, project_name: str = None) -> Dict:
        """
        Retrieve details for the specified executed task id.
        Args:
            task_id (int): ID of the executed Matillion task.
            project_name (str): Name of the Matillion project.
        Returns:
            dict : Sample response can be found at https://documentation.matillion.com/docs/2972278
        """
        self._ensure_attributes(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        return self._api_request(
            API_GET,
            "group",
            "name",
            self.project_group_name,
            "project",
            "name",
            project_name if project_name else self.project_name,
            "task",
            "id",
            str(task_id),
        ).json()

    def delete_project(self, project_name: str, version: str = DEFAULT_VERSION) -> Dict:
        """
        Delete Matillion project. If version is specified then delete specified project version.

        Args:
            project_name (str): Name of the Matillion project.
            version: (str), optional. Default value : default.
        Returns:
            dict : Sample response can be found at https://documentation.matillion.com/docs/2949951#deleting-resources
        """
        self._ensure_attributes(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        return self._api_request(
            API_POST,
            "group",
            "name",
            self.project_group_name,
            "project",
            "name",
            project_name if project_name else self.project_name,
            "version",
            "name",
            version,
            "delete",
        ).json()

    def delete_job(
        self, job_name: str, project_name: str = None, version: str = DEFAULT_VERSION
    ) -> Dict:
        """
        Delete Matillion job within the specified version of the project.

        Args:
            job_name: (str), required. Name of the Matillion job to delete.
            project_name: (str), optional. Name of the Matillion project.
            version: (str), optional. Default value : default.
        Returns:
            Dict[Any, Any] : Sample response can be found at https://documentation.matillion.com/docs/2949951#deleting-resources
        """
        self._ensure_attributes(
            BASE_URL, USERNAME, PASSWORD, PROJECT_GROUP_NAME, PROJECT_NAME
        )
        return self._api_request(
            API_POST,
            "group",
            "name",
            self.project_group_name,
            "project",
            "name",
            project_name if project_name else self.project_name,
            "version",
            "name",
            version,
            "job",
            "name",
            job_name,
            "delete",
        ).json()
