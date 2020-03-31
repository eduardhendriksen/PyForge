# -*- coding: utf-8 -*-
"""Module containing classes related to business units on the Autodesk Forge BIM360 platform."""
import requests


class BusinessUnitsApi():
    """This class provides the base API calls for Autodesk BIM360 business units."""

    def __init__(self, token=None):
        """
        Initialize the BusinessUnitsApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            :None.

        """
        self.token = token

    def get_account_business_units(self, token=None, account_id=None,
                             url=r' https://developer.api.autodesk.com/hq/v1/accounts/:account_id/business_units_structure'):
        """
        Send a GET accounts/:account_id/business_units_structure request to the BIM360 API, returns the business units available to the Autodesk account on the given account.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            :account_id (str, optional): The account id for the BIM360 account. Defaults to None.
            :limit (int, optional): Size of the response array. Defaults to 100.
            :offset (int, optional): Offset of the response array. Defaults to 0.
            :sort (list, optional): List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].
            :field (list, optional): List of string field names to include in the response array. Defaults to [].
            :url (str, optional):  url endpoint for the GET accounts/:account_id/business units request.
                Currently default is pointed at the US BIM360 servers.
                EMEA server:   https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/business_units_structure
                Defaults to  https://developer.api.autodesk.com/hq/v1/accounts/:account_id/business_units_structure.

        Raises:
            :ValueError: If any of token and self.token, account_id are of NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if account_id is None:
            raise ValueError("Please enter a account id.")

        url = url.replace(':account_id', account_id)

        resp = requests.request('GET',
                                url,
                                headers={'Authorization' : "Bearer {}".format(token)},
                                timeout=12)

        if resp.status_code == 200:

            cont = resp.json()['business_units']

            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content))