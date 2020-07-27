# -*- coding: utf-8 -*-
"""Module containing classes related to business units on the Autodesk Forge BIM360 platform."""
import requests
from PyForge.ForgeApi import ForgeApi


class BusinessUnitsApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 business units."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/hq/v1/accounts/',
                 timeout=1):
        """
        Initialize the BusinessUnitsApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the model derivative API.
                Defaults to r'https://developer.api.autodesk.com/hq/v1/accounts/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_account_business_units(self, account_id=None, endpoint=r':account_id/business_units_structure'):
        """
        Send a GET accounts/:account_id/business_units_structure request to the BIM360 API, returns the business units available to the Autodesk account on the given account.

        Args:
            account_id (str, optional): The account id for the BIM360 account. Defaults to None.
            endpoint (str, optional): url endpoint for the GET accounts/:account_id/business_units_structure request. Defaults to r':account_id/business_units_structure'.

        Raises:
            ValueError: If self.token, account_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the BusinessUnitsApi.")

        if account_id is None:
            raise ValueError("Please enter a account id.")

        endpoint = endpoint.replace(':account_id', account_id)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:

            cont = resp.json()['business_units']

            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))