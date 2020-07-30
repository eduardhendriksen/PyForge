# -*- coding: utf-8 -*-
"""Module containing classes related to item versions on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi
from urllib.parse import quote_plus


class VersionsApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 versions."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/data/v1/projects/',
                 timeout=1):
        """
        Initialize the VersionsApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the versions API.
                Defaults to r'https://developer.api.autodesk.com/data/v1/projects/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.
        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_version(self, project_id, version_id,
                    endpoint=r':project_id/versions/:version_id'):
        """
        Send a GET projects/:project_id/versions/:version_id request to the BIM360 API, returns the version corresponding to the version id.

        Args:
            project_id: The project id for the project the folder is in.
            version_id (str): Version id of the version to be obtained
            endpoint (str, optional): endpoint for the GET projects/:project_id/versions/:version_id request.
            Defaults to r':project_id/versions/:version_id'.

        Raises:
            ValueError: If self.token, project_id or version_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            dict(JsonApiObject): Version JsonApi object in the form of a dict.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the VersionsApi.")

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if not project_id.startswith("b."):
            project_id = "b.{}".format(project_id)

        if version_id is None:
            raise ValueError("Please enter a version id.")

        endpoint = endpoint.replace(':project_id', project_id).replace(':version_id', quote_plus(version_id))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            cont = resp.json()
            return cont['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))