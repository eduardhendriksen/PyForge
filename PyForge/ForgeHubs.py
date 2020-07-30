# -*- coding: utf-8 -*-
"""Module containing classes related to hubs on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi

class HubsApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 hubs."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/project/v1/',
                 timeout=1):
        """
        Initialize the HubsApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the hubs API.
                Defaults to r'https://developer.api.autodesk.com/project/v1/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_hubs(self, endpoint=r'hubs'):
        """
        Send a GET hubs request to the BIM360 API, returns the hubs available to the Autodesk account.

        Args:
            endpoint (str, optional): endpoint for the GET hubs request. Defaults to r'hubs'.

        Raises:
            ValueError: If self.token is of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            list(dict(JsonApiObject)): List of hub JsonApi objects in the form of dicts.

        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the HubsApi.")

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            cont = resp.json()
            return (cont['data'])

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))
