# -*- coding: utf-8 -*-
"""Module containing classes related to hubs on the Autodesk Forge BIM360 platform."""
import requests


class HubsApi():
    """This class provides the base API calls for Autodesk BIM360 hubs."""

    def __init__(self, token=None):
        """
        Initialize the HubsApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            :None.

        """
        self.token = token

    def get_hubs(self, token=None, url=r'https://developer.api.autodesk.com/project/v1/hubs'):
        """
        Send a GET hubs request to the BIM360 API, returns the hubs available to the Autodesk account.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            :url (str, optional): Url endpoint for the GET hubs request. Defaults to r'https://developer.api.autodesk.com/project/v1/hubs'.

        Raises:
            :ValueError: If all of token and self.token are of NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :list(dict(JsonApiObject)): List of hub JsonApi objects in the form of dicts.

        """
        method = 'GET'

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")
        else:
            if self.token is not None:
                token = self.token

        headers = { 'Authorization' : "Bearer {}".format(token) }

        resp = requests.request(method ,
                                url,
                                headers=headers,
                                timeout=12)

        if resp.status_code == 200:
            cont = resp.json()
            return (cont['data'])
        else:
            if resp.status_code == 401:
                raise ConnectionError("Renew authorization token.")
            else:
                raise ConnectionError("Request failed with " +
                                      "code {}".format(resp.status_code) +
                                      " and message :" +
                                      "{}".format(resp.content))
