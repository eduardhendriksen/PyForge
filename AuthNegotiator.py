# -*- coding: utf-8 -*-
"""Module containing classes related to authentication on the Autodesk Forge BIM360 platform."""
import requests


class OAuth2Negotiator():
    """Class to negotiate the authentication with the Autodesk Forge Api Authentication servers."""

    def __init__(self, webAddress, clientId, clientSecret, scopes, redirectAddress=None, endAddress=None):
        """
        Initialize the OAuth2Negotiator class and assign the needed parameters for authentication.

        Args:
            :webAddress (str): Web address for the Autodesk Forge API authentication server.
            :clientId (str): Client id for the Forge App this authentication is used for.
            :clientSecret (str): Client secret for the Forge App this authentication is used for.
            :scopes (list, str): API access scopes requested in the authentication.
            :redirectAddress (str, optional): Redirect web address used for 3-legged authentication. Defaults to None.
            :endAddress (str, optional): End web address to redirect to after 3-legged authentication has succeeded. Defaults to None.

        Raises:
            :TypeError: If the type of the scopes argument is not list of str this error is raised.

        Returns:
            :None.

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

    def get_token(self, legs=2):
        """
        Contact the Autodesk Forge API Authentication server and obtain an access token.

        Args:
            :legs (int, optional): Indicates if 2- or 3-legged authentication is used. Defaults to 2.

        Raises:
            :ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            :str: Autodesk Forge acces token.
            :int: Time in s that the token stays active.

        """
        if legs == 2:

            method = 'POST'
            headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
            data = { 'client_id' : self.clientId,
                       'client_secret' : self.clientSecret,
                       'grant_type' : 'client_credentials',
                       'scope' : self.scopes }


            resp = requests.request(method ,
                                    self.webAddress,
                                    headers=headers,
                                    data=data,
                                    timeout=12)

            if resp.status_code == 200:
                cont = resp.json()
                return (cont['access_token'], cont['expires_in'])
            else:
                if resp.status_code in [429, 500]:
                    raise ConnectionError("Connection to auth server not " +
                                          "made, please try again.")
                else:
                    raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                                          " and message : {}".format(resp.content))
        else:
            pass