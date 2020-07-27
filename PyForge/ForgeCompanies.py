# -*- coding: utf-8 -*-
"""Module containing classes related to companies on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi


class CompaniesApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 companies."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/hq/v1/accounts/',
                 timeout=1):
        """
        Initialize the CompaniesApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the model derivative API.
                Defaults to r'https://developer.api.autodesk.com/hq/v1/accounts/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_account_companies(self, account_id=None, limit=100, offset=0, sort=[], field=[],
                              endpoint=r':account_id/companies'):
        """
        Send a GET accounts/:account_id/companies request to the BIM360 API, returns the companies available to the Autodesk account on the given account.

        Args:
            account_id (str, optional): The account id for the BIM360 account. Defaults to None.
            limit (int, optional): Size of the response array. Defaults to 100.
            offset (int, optional): Offset of the response array. Defaults to 0.
            sort (list, optional): List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].
            field (list, optional): List of string field names to include in the response array. Defaults to [].
            endpoint (str, optional):  endpoint for the GET accounts/:account_id/companies request. Defaults to: r':account_id/companies'

        Raises:
            ValueError: If any of token and self.token, account_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the CompaniesApi.")

        if account_id is None:
            raise ValueError("Please enter a account id.")

        endpoint = endpoint.replace(':account_id', account_id)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        params = {}

        params.update({'limit' : limit})
        params.update({'offset' : offset})

        if sort:
            sort = ",".join(sort)
            params.update({'sort' : sort})
        if field:
            field = ",".join(field)
            params.update({'field' : field})

        resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            cont = resp.json()

            if isinstance(cont, list):
                if len(cont) == limit:
                    cont += self.get_account_companies(account_id=account_id,
                                                       limit=limit,
                                                       offset=offset+limit,
                                                       sort=sort,
                                                       field=field,
                                                       url=url)

                return cont
            else:
                print(cont)

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))