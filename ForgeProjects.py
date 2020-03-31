# -*- coding: utf-8 -*-

import requests


class ProjectsApi():
    """
    This class provides the base API calls for Autodesk BIM360 projects.
    """

    def __init__(self, token=None):
        """
        Initialize the ProjectsApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            :None.

        """
        self.token = token

    def get_hub_projects(self, token=None, hub_id=None, url=r'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects'):
        """
        Sends a GET hubs/:hub_id/projects request to the BIM360 API, returns the projects available to the Autodesk account on the given
        hub.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            :hub_id (str, optional): The hub id for the hub. Defaults to None.
            :url (str, optional): url endpoint for the GET hubs/:hub_id/projects request.
            Defaults to r'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects'.

        Raises:
            :ValueError: If any of token and self.token, hub_id are of NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :list(dict(JsonApiObject)): List of project JsonApi objects in the form of dicts.

        """

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if hub_id is None:
            raise ValueError("Please enter a hub id.")

        url = url.replace(':hub_id', hub_id)

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
