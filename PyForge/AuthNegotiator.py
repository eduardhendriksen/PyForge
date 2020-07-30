# -*- coding: utf-8 -*-
"""Module containing classes related to authentication on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi

class OAuth2Negotiator(ForgeApi):
    """Class to negotiate the authentication with the Autodesk Forge Api Authentication servers."""

    def __init__(self, webAddress, clientId, clientSecret, scopes, redirectAddress=None, endAddress=None, timeout=1):
        """
        Initialize the OAuth2Negotiator class and assign the needed parameters for authentication.

        Args:
            webAddress (str): Web address for the Autodesk Forge API authentication server.
            clientId (str): Client id for the Forge App this authentication is used for.
            clientSecret (str): Client secret for the Forge App this authentication is used for.
            scopes (list, str): API access scopes requested in the authentication.
            redirectAddress (str, optional): Redirect web address used for 3-legged authentication. Defaults to None.
            endAddress (str, optional): End web address to redirect to after 3-legged authentication has succeeded. Defaults to None.
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Raises:
            TypeError: If the type of the scopes argument is not list of str this error is raised.

        Returns:
            None.

        """
        self.webAddress = webAddress
        self.redirectAddress = redirectAddress
        self.clientId = clientId
        self.clientSecret = clientSecret

        if type(scopes) == list:
            self.scopes = ''
            for scope in scopes:
                self.scopes += "{} ".format(scope)
        elif type(scopes) == str:
            self.scopes = scopes
        else:
            raise TypeError(scopes)

        self.endAddress = endAddress

        super().__init__(self, base_url=webAddress, timeout=timeout)

    def get_token(self, legs=2):
        """
        Contact the Autodesk Forge API Authentication server and obtain an access token.

        Args:
            legs (int, optional): Indicates if 2- or 3-legged authentication is used. Defaults to 2.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            str: Autodesk Forge acces token.
            int: Time in s that the token stays active.

        """
        if legs == 2:

            headers = {}

            headers.update({ 'Content-Type' : 'application/x-www-form-urlencoded' })

            data = {}

            data.update({'client_id' : self.clientId})
            data.update({'client_secret' : self.clientSecret})
            data.update({'grant_type' : 'client_credentials'})
            data.update({'scope' : self.scopes})

            resp = self.http.post(self.webAddress, headers=headers, data=data)

            if resp.status_code == 200:
                cont = resp.json()
                return (cont['access_token'], cont['expires_in'])

            raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                                  " and message : {}".format(resp.content) +
                                  " during authentication.")
        else:
            raise NotImplementedError("3-legged authentication has not been implemented.")