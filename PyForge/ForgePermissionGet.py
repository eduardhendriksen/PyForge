# -*- coding: utf-8 -*-
"""Module containing classes related to folders on the Autodesk Forge BIM360 platform."""
import re
from PyForge.ForgeApi import ForgeApi


class PermissionApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 folder permissions."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/',
                 timeout=1):
        """
        Initialize the PermissionApi class and attach an authentication token for the Autodesk Forge API.
        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the model derivative API.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.
        Returns:
            None.
        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_folder_permission(self, project_id, folder_id,
                              endpoint=r':project_id/folders/:folder_id/permissions'):
        """
        Send a GET projects/:project_id/folders/:folder_id request to the BIM360 API, returns a json list containing the permissions on the folder.
        Args:
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            endpoint (str, optional): endpoint for the GET projects/:project_id/folders/:folder_id request.
                Defaults to r':project_id/folders/:folder_id/permissions'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            response json object.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the PermissionApi.")

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if project_id.startswith("b."):
            project_id = project_id[2:]

        if folder_id is None:
            raise ValueError("Please enter a folder id.")

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        endpoint = endpoint.replace(':project_id', project_id).replace(':folder_id', folder_id)

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            cont = resp.json()
            return cont

        if resp.status_code == 400:
            raise ConnectionError(resp.content)

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

