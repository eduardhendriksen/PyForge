# -*- coding: utf-8 -*-
"""Module containing classes related to BIM 360 Document Management folder (POST), including details about the name and the status."""
import re
import requests


class PostPermissionApi():

    """This class provides the base API calls permission for Autodesk BIM 360 Document Management folder."""

    def __init__(self, token, subjectId, subjectType, actions):
        """
        Initialize the PostPermissionApi class and assign the needed parameters for authentication.

        Args:

            subjectId (str): subjectId of the user, role, or company.
            subjectType (str): The type of subject. Possible values: USER, COMPANY, ROLE
            actions (list, str): Permitted actions for the user, role, or company.
                                The six permission levels in BIM 360 Document Managment correspond to one or more actions.
        Raises:
            TypeError: If the type of the actions argument is not list of str this error is raised.

        Returns:
            None.

        """
        self.token = token
        self.subjectId = subjectId
        self.subjectType = subjectType

        if type(actions) == list:
            self.actions = ''
            for action in actions:
                self.actions += "{} ".format(action)
        elif type(actions) == str:
            self.actions = actions
        else:
            raise TypeError(actions)


    def get_folder_permission_batch_create(self, token, project_id, folder_id,
                   url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-create'):
        """
        Assign permissions to multiple users, roles, and companies for a BIM 360 Document Management folder.
        Send a POST projects/:project_id/folders/:folder_id request to the BIM 360 Document Management folder, returns the results JsonApiObject available to the Autodesk account on the given project id for the given folder id .
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            url (str, optional): url endpoint for the GET projects/:project_id/folders/:folder_id request.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-create'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): JsonApi Folder object in the form of a dict.
        """
        method = 'POST'

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

        headers = {'Authorization' : "Bearer {}".format(token),
                   'Content-Type' : 'application/json'}
        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)
        data = { 'subjectId' : self.subjectId,
                  'subjectType' : self.subjectType,
                   'actions' : self.actions }

        resp = requests.request(method,
                                url,
                                headers=headers,
                                body=data,
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

    def get_folder_permission_batch_update(self, token, project_id, folder_id,
                   url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-update'):
        """
        Updates the permissions assigned to multiple users, roles, and companies for a folder. This endpoint replaces the permissions that were previously assigned to the user for this folder.
        Send a POST bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-update request to the BIM 360 Document Management folder, returns the result updated JsonApiObject available to the Autodesk account on the given project id for the given folder id.
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            url (str, optional): url endpoint for the POST projects/:project_id/folders/:folder_id/permissions:batch-update request.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-update'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): JsonApi Folder object in the form of a dict.
        """
        method = 'POST'

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

        headers = {'Authorization' : "Bearer {}".format(token),
                   'Content-Type' : 'application/json'}
        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)
        data = { 'subjectId' : self.subjectId,
                    'subjectType' : self.subjectType,
                      'actions' : self.actions }

        resp = requests.request(method,
                                url,
                                headers=headers,
                                data=data,
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


    def get_folder_permission_batch_delete(self, token, project_id, folder_id,
                   url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-delete'):
        """
        Deletes all the permissions assigned to specified users, roles, and companies.
        Note that you cannot delete permission for project admins, who are always assigned full permissions.
        Send a POST bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-delete request to BIM 360 Document Management folder, returns No response!
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            url (str, optional): url endpoint for the post projects/:project_id/folders/:folder_id/permissions:batch-delete request.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-delete'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): JsonApi Folder object in the form of a dict.
        """
        method = 'POST'

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

        headers = {'Authorization' : "Bearer {}".format(token),
                   'Content-Type' : 'application/json'}
        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)
        data = { 'subjectId' : self.subjectId,
                  'subjectType' : self.subjectType}

        resp = requests.request(method,
                                url,
                                headers=headers,
                                data=data,
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

