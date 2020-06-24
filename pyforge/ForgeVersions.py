# -*- coding: utf-8 -*-
"""Module containing classes related to item versions on the Autodesk Forge BIM360 platform."""
import requests
from urllib.parse import quote_plus


class VersionsApi():
    """This class provides the base API calls for Autodesk BIM360 versions."""

    def __init__(self, token=None):
        """
        Initialize the VersionsApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            None.
        """
        self.token = token

    def get_version(self, token, project_id, version_id,
                    url=r'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id'):
        """
        Send a GET projects/:project_id/versions/:version_id request to the BIM360 API, returns the version corresponding to the version id.

        Args:
            token: Authentication token for Autodesk Forge API.
            project_id: The project id for the project the folder is in.
            version_id (str): Version id of the version to be obtained
            url (str, optional): url endpoint for the GET projects/:project_id/versions/:version_id request.
            Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id'.

        Returns:
            dict(JsonApiObject): Version JsonApi object in the form of a dict.

        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if not project_id.startswith("b."):
            project_id = "b.{}".format(project_id)

        if version_id is None:
            raise ValueError("Please enter a version id.")

        url = url.replace(':project_id', project_id).replace(':version_id', quote_plus(version_id))

        resp = requests.request('GET',
                                url,
                                headers={'Authorization' : "Bearer {}".format(token)},
                                timeout=12)

        if resp.status_code == 200:
            cont = resp.json()
            return cont['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with " +
                              "code {}".format(resp.status_code) +
                              " and message :" +
                              "{}".format(resp.content))
