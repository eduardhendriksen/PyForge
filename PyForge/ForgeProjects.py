# -*- coding: utf-8 -*-
"""Module containing classes related to projects on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi


class ProjectsApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 projects."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/project/v1/hubs/',
                 timeout=1):
        """
        Initialize the ProjectsApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the projects API.
                Defaults to r'https://developer.api.autodesk.com/project/v1/hubs/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.
        Returns:
            None.
        """
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_account_projects(self, account_id, limit=100,
                             endpoint=r':hub_id/projects'):
        """
        Send a GET hubs/:hub_id/projects // GET accounts/:account_id/projects request to the BIM360 API, returns the projects available to the Autodesk account on the given account.

        Args:
            account_id (str): The account id // hub id for the BIM360 account. They are related in the form hub_id = "b." + account_id
            limit (int, optional): Size of the response array. Defaults to 100.
            offset (int, optional): Offset of the response array. Defaults to 0.
            sort (list, optional): List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].
            field (list, optional): List of string field names to include in the response array. Defaults to [].
            endpoint (str, optional):  endpoint for the GET accounts/:account_id/projects request.
                Defaults to r':account_id/projects'.
        Raises:
            ValueError: If any self.token and account_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            list(dict(JsonApiObject)): List of project JsonApi objects in the form of dicts.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ProjectsApi.")

        if account_id is None:
            raise ValueError("Please enter a account id.")

        if not account_id.startswith("b."):
            account_id = "b.{}".format(account_id)

        endpoint = endpoint.replace(':hub_id', account_id)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        params = {}

        params.update({'page[limit]' : limit})

        next_page = -1
        data = []

        while next_page != 0:

            if next_page > 0:

                params.update({'page[number]' : str(next_page)})

                resp = self.http.get(endpoint, headers=headers, params=params)

            else:

                resp = self.http.get(endpoint, headers=headers, params=params)

            if resp.status_code == 200:

                cont = resp.json()
                data += cont['data']

                try:
                    match = re.search(r'page%5Bnumber%5D=(\d+)', cont['links']['next']['href'])

                    if match is not None:
                        next_page = int(match.groups()[0])
                    else:
                        return data

                except KeyError:

                    return data

            else:
                if resp.status_code == 401:
                    raise ConnectionError("Renew authorization token.")

                raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                                      " and message : {}".format(resp.content) +
                                      " for endpoint: {}".format(endpoint))
