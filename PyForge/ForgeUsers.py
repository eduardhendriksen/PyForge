# -*- coding: utf-8 -*-
"""Module containing classes related to users on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi


class UsersApi(ForgeApi):
    """This class provides the base API calls for Autodesk BIM360 users."""

    def __init__(self, token,
                 base_url=r'https://developer.api.autodesk.com/bim360/admin/v1/',
                 timeout=1):
        """
        Initialize the UsersApi class and attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the users API.
                Defaults to r'https://developer.api.autodesk.com/bim360/admin/v1/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        self.token = token

    def get_project_users(self, project_id=None, region='US', accept_language="de", filters={},
                          limit=100, offset=0, sort=[], fields=[],
                          endpoint=r'projects/:projectId/users'):
        """
        Send a GET projects/:projectId/users request to the BIM360 API, returns the users assigned to the project.

        Args:
            project_id (str, optional): The project id for the BIM360 project. Defaults to None.
            region (str, optional): The BIM360 server region to be adressed, can be US or EMEA. Defaults to US.
            accept_language (str, optional): The language in which the response is to be returned. Defaults to de.
            filters (dict, optional): A dict of filters in the form {filtertype : List(str filter entries)}. Defaults to {}.
            limit (int, optional): Size of the response array. Defaults to 100.
            offset (int, optional): Offset of the response array. Defaults to 0.
            sort (list, optional): List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].
            fields (list, optional): List of string field names to include in the response array. Defaults to [].
            endpoint (str, optional):  endpoint for the GET projects/:projectId/users request.
                Defaults to r'projects/:projectId/users'

        Raises:
            ValueError: If self.token, project_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            list(dict(JsonApiObject)): List of users JsonApi objects in the form of dicts.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the UsersApi.")

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if project_id.startswith("b."):
            project_id = project_id[2:]

        endpoint = endpoint.replace(':projectId', project_id)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        headers.update({'Accept-Language' : accept_language})
        headers.update({'Region' : region})

        params = {}

        params.update({'limit' : limit})
        params.update({'offset' : offset})

        params.update(self.make_filters(filters))

        if sort:
            sort = ",".join(sort)
            params.update({'sort' : sort})
        if fields:
            fields = ",".join(fields)
            params.update({'field' : fields})

        resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            cont = resp.json()['results']

            if isinstance(cont, list):

                if len(cont) == limit:
                    cont += self.get_account_projects(token=token,
                                                      project_id=project_id,
                                                      region=region,
                                                      accept_language=accept_language,
                                                      filters=filters,
                                                      limit=limit,
                                                      offset=offset+limit,
                                                      sort=sort,
                                                      fields=fields,
                                                      url=url)

                return cont
            else:
                raise TypeError(f"Invalid response type for endpoint: {endpoint}\n" +
                                f"with content: {resp.content}")

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def make_filters(self, filters):
        """
        Create a filter query parameter of the given type with the given entries.

        Args:
            filters (dict, {str, filter_name : list(str, filter entires)}): The filters to be used.

        Raises:
            ValueError: Raised if the filter entries exceed 255 characters.
            TypeError: Raised if the filters parameter is not of type dict.

        Returns:
            dict: A filter dictionary to be used as a query parameter.
        """
        if isinstance(filters, dict):
            if filters:
                for filt, entries in filters.items():
                    things = ",".join(entries)
                    if len(things) > 255:
                        raise ValueError("Max filterlength is 255 characters.")
                    return {"filter[{}]".format(filt) : things}
            else:
                return {}

        raise TypeError("filters parameter has the wrong type: {}".format(type(filters)))
