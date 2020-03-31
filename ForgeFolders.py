# -*- coding: utf-8 -*-

import re
import requests


class FoldersApi():
    """
    This class provides the base API calls for Autodesk BIM360 folders.
    """

    def __init__(self, token=None):
        """
        Initialize the FoldersApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            :token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            :None.

        """

        self.token = token

    def get_folder_contents(self, token=None, project_id=None, folder_id=None, type_filter=None,
                            url=r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/contents'):
        """
        Sends a GET projects/:project_id/folders/:folder_id/contents request to the BIM360 API, returns the folder contents available
        to the Autodesk account on the given hub.

        Args:
            :token (str): Authentication token for Autodesk Forge API.
            :project_id (str): The project id for the project the folder is in.
            :folder_id (str): The folder id for the folder.
            :type_filter (str, list): BIM360 item type or list of BIM360 item types to filter for.
            :url (str): url endpoint for the GET projects/:project_id/folders/:folder_id/contents request.

        Raises:
            :ValueError: If any of token and self.token, project_id or folder_id are NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :list(dict(JsonApiObject)): List of JsonApi Data objects in the form of dicts.
            :list(dict(JsonApiObject)): List of JsonApi Version objects in the form of dicts.
        """

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if not project_id.startswith("b."):
            project_id = "b.{}".format(project_id)

        if folder_id is None:
            raise ValueError("Please enter a folder id.")

        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)
        params = {}

        if type_filter is not None:
            params.update(self.make_filter_param(type_filter, "type"))

        next_page = -1
        data = []
        included = []

        while next_page != 0:

            if next_page > 0:

                params.update({'page[number]' : str(next_page)})

                resp = requests.request('GET',
                                        url,
                                        params=params,
                                        headers={'Authorization' : "Bearer {}".format(token)},
                                        timeout=12)

            else:

                resp = requests.request('GET',
                                        url,
                                        params=params,
                                        headers={'Authorization' : "Bearer {}".format(token)},
                                        timeout=12)

            if resp.status_code == 200:

                cont = resp.json()
                data += cont['data']

                try:
                    included += cont['included']
                except KeyError:
                    pass

                try:

                    match = re.search(r'page%5Bnumber%5D=(\d+)', cont['links']['next']['href'])

                    if match is not None:
                        next_page = int(match.groups()[0])
                    else:
                        return data, included

                except KeyError:

                    return data, included

            else:
                if resp.status_code == 401:
                    raise ConnectionError("Renew authorization token.")

                raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                                      " and message :{}".format(resp.content))

    def get_folder(self, token, project_id, folder_id,
                   url=r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'):
        """
        Sends a GET projects/:project_id/folders/:folder_id request to the BIM360 API, returns the folder JsonApiObject available
        to the Autodesk account on the given hub for the given project id.

        Args:
            :token (str): Authentication token for Autodesk Forge API.
            :project_id (str): The project id for the project the folder is in.
            :folder_id (str): The folder id for the folder.
            :url (str, optional): url endpoint for the GET projects/:project_id/folders/:folder_id request. Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'.

        Raises:
            :ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :dict(JsonApiObject): JsonApi Folder object in the form of a dict.
        """


        method = 'GET'

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if not project_id.startswith("b."):
            project_id = "b.{}".format(project_id)

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
            return cont['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with " +
                              "code {}".format(resp.status_code) +
                              " and message :" +
                              "{}".format(resp.content))

    def search_folder(self, token, project_id, folder_id, search_filter, type_filter,
                      url=r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'):
        """
        Sends a GET projects/:project_id/folders/:folder_id/search request to the BIM360 API, recursively searching the folder and
        subfolders for the given search filter. Returns the search results data JsonApi Objects available to the user in the given search.

        Args:
            :token (str): Authentication token for Autodesk Forge API. Must be 3-legged with data:search scope requested.
            :project_id (str): The project id for the project the folder to be searched is in.
            :folder_id (str): The folder id for the folder to be searched.
            :search_filter (str, list): The filter(s) to search for.
            :type_filter (str, list): Autodesk item type filter(s).
            :url (TYPE, optional): Url endpoint for the GET projects/:project_id/folders/:folder_id request. Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'.

        Raises:
            :ValueError: If any of token and self.token, project_id or folder_id are NoneType.
            :TypeError: If search filter is of NoneType.
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :list(dict(JsonApiObject)): List of JsonApi Data objects in the form of dicts.
            :list(dict(JsonApiObject)): List of JsonApi Version objects in the form of dicts.

        """

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if not project_id.startswith("b."):
            project_id = "b.{}".format(project_id)

        if folder_id is None:
            raise ValueError("Please enter a folder id.")

        url = url.replace(':project_id', project_id).replace(':folder_id', folder_id)
        params = {}

        if search_filter is not None:
            params.update(self.make_filter_param(search_filter, "name"))
        else:
            raise TypeError("Search filter can not be NoneType")

        if type_filter is not None:
            params.update(self.make_filter_param(type_filter, "type"))

        next_page = -1
        data = []
        included = []

        while next_page != 0:

            if next_page > 0:

                params.update({'next[page]' : str(next_page)})

                resp = requests.request('GET',
                                        url,
                                        params=params,
                                        headers={'Authorization' : "Bearer {}".format(token)},
                                        timeout=12)

            else:

                resp = requests.request('GET',
                                        url,
                                        params=params,
                                        headers={'Authorization' : "Bearer {}".format(token)},
                                        timeout=12)

            if resp.status_code == 200:

                cont = resp.json()
                data += cont['data']

                try:
                    included += cont['included']
                except KeyError:
                    pass

                try:
                    match = re.search(r'page%5Bnumber%5D=(\d+)', cont['links']['next']['href'])

                    if match is not None:
                        next_page = int(match.groups()[0])
                    else:
                        return data, included

                except KeyError:

                    return data, included

            else:
                if resp.status_code == 401:
                    raise ConnectionError("Renew authorization token.")

                raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                                      " and message :{}".format(resp.content))

    def make_filter_param(self, filter_entries, filter_type):
        """
        This utility method creates a filter query parameter of the given type with the given entries.

        Args:
            :filter_entries (str, list): The entries to be filtered for.
            :filter_type (str): The type of filter to be made.

        Raises:
            :TypeError: Raised if the filter_entries parameter is not of type str or list.

        Returns:
            :dict: A filter dictionary to be used as a query parameter.

        """

        if isinstance(filter_entries, list):
            things = ''
            for thing in filter_entries:
                if filter_entries.index(thing) != len(filter_entries) - 1:
                    things += "{},".format(thing)
                else:
                    things += "{}".format(thing)
            return {"filter[{}]".format(filter_type) : things}
        if isinstance(filter_entries, str):
            return {"filter[{}]".format(filter_type) : filter_entries}

        raise TypeError("filter_entries parameter has the wrong type: {}".format(type(filter_entries)))
