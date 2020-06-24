
# coding: utf-8

# In[30]:



"""Module containing classes related to folders on the Autodesk Forge BIM360 platform."""
import re
import requests


class PermissionApi():
    """This class provides the base API calls for Autodesk BIM360 folders."""

    def __init__(self, token=None):
        """
        Initialize the PermissionApi class and optionally attach an authentication token for the Autodesk Forge API.
        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
        Returns:
            None.
        """
        self.token = token

    def get_folder_permission(self, token, project_id, folder_id,
                   url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions'):
        """
        Send a GET projects/:project_id/folders/:folder_id request to the BIM360 API, returns the folder JsonApiObject available to the Autodesk account on the given hub for the given project id.
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            url (str, optional): url endpoint for the GET projects/:project_id/folders/:folder_id request.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): JsonApi Folder object in the form of a dict.
        """
        method = 'GET'

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if project_id.startswith("b."):
            project_id = project_id[2:]

        if folder_id is None:
            raise ValueError("Please enter a folder id.")

        headers = {'Authorization' : "Bearer {}".format(token)}
        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)

        resp = requests.request(method,
                                url,
                                headers=headers,
                                timeout=12)

        if resp.status_code == 200:
            cont = resp.json()
            return cont
        
        if resp.status_code == 400:
            raise ConnectionError(resp.content)

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content))        

