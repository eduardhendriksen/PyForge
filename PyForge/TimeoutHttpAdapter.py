# -*- coding: utf-8 -*-
"""Module containing the timeout http adapter for the PyForge package."""
from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT = 0.5 # seconds

class TimeoutHttpAdapter(HTTPAdapter):
    """Implementation of the HTTPAdapter class implementing default timeouts."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the TimeoutHttpAdapter class with a standard timeout.

        Args:
            timeout (float, optional): Default timeout for API calls. Defaults to DEFAULT_TIMEOUT.

        Returns:
            None.
        """
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """
        Adds the default timeout to all requests sent using the adapter.

        Args:
            request: http request.

        Returns:
            request: with timeout attached.
        """        ""
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
