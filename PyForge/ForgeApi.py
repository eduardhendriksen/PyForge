# -*- coding: utf-8 -*-
"""Module containing the base Api class for the Autodesk Forge platform."""
from urllib3.util.retry import Retry
from requests_toolbelt import sessions
from PyForge.TimeoutHttpAdapter import TimeoutHttpAdapter

class ForgeApi():
    """This class provides the base class for API calls for Autodesk Forge."""

    def __init__(self, token=None,
                 base_url=r'https://developer.api.autodesk.com/',
                 timeout=1):
        """
        Initialize the ForgeApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the model derivative API.
                Defaults to r'https://developer.api.autodesk.com/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        self.token = token
        self.http = sessions.BaseUrlSession(base_url)
        self.http.hooks['response'] = [lambda response, *args, **kwargs: response.raise_for_status()]
        retries = Retry(total=6, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = TimeoutHttpAdapter(timeout=timeout, max_retries=retries)
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)