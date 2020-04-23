# -*- coding: utf-8 -*-
"""Module containing classes related to deriving model data from the Autodesk Forge BIM360 platform."""
import requests
import base64
from urllib.parse import quote_plus


class ModelDerivativeApi():
    """This class provides the base API calls for Autodesk BIM360 model derivatives."""

    def __init__(self, token=None):
        """
        Initialize the ModelDerivativeApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.

        Returns:
            None.

        """
        self.token = token

    def get_manifest(self, token=None, urn=None, accept_encoding=None,
                     url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/manifest'):
        """
        Send a GET :urn/metadata request to the BIM360 API, returns information about derivatives that correspond to a specific source file, including derivative URNs and statuses.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            url (str, optional):  url endpoint for the GET :urn/metadata.
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/manifest'

        Raises:
            ValueError: If any of token and self.token, urn are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        url = url.replace(':urn', urn.decode('utf8'))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})

        outstanding = True
        while outstanding:
            try:
                resp = requests.request('GET',
                                        url,
                                        headers=headers,
                                        timeout=2.5)
                outstanding = False
            except requests.exceptions.ReadTimeout:
                resp = requests.request('GET',
                                        url,
                                        headers=headers,
                                        timeout=2.5)
                outstanding = False

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for url: {}".format(url))

    def get_derivative(self, token=None, urn=None, derivative_urn=None,
                       url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/manifest/:derivativeUrn'):
        """
        Send a GET  :urn/manifest/:derivativeurn request to the BIM360 API, Downloads a selected derivative.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            derivative_urn (str, optional): The urn for the chosen derivative. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            url (str, optional):  url endpoint for the GET :urn/metadata/:guid.
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/manifest/:derivativeUrn'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        url = url.replace(':urn', urn.decode('utf8'))

        url = url.replace(':derivativeUrn', quote_plus(derivative_urn))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        resp = requests.request('GET',
                                url,
                                headers=headers)

        while resp.status_code == 202:
            resp = requests.request('GET',
                                    url,
                                    headers=headers)

        if resp.status_code == 200:
            return resp

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for url: {}".format(url))

    def get_metadata_ids(self, token=None, urn=None, accept_encoding=None,
                          url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata'):
        """
        Send a GET :urn/metadata request to the BIM360 API, returns the available metadata ID's for the model.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            url (str, optional):  url endpoint for the GET :urn/metadata.
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata'

        Raises:
            ValueError: If any of token and self.token, urn are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        url = url.replace(':urn', urn.decode('utf8'))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})

        outstanding = True
        while outstanding:
            try:
                resp = requests.request('GET',
                                        url,
                                        headers=headers,
                                        timeout=2.5)
                outstanding = False
            except requests.exceptions.ReadTimeout:
                resp = requests.request('GET',
                                        url,
                                        headers=headers,
                                        timeout=2.5)
                outstanding = False

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for url: {}".format(url))

    def get_object_tree(self, token=None, urn=None, guid=None, accept_encoding=None, x_ads_force='true',
                          url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid'):
        """
        Send a GET :urn/metadata/:guid request to the BIM360 API, returns the object tree for the given metadata id (corresponding to a model view) for the model.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            guid (str, optional): The guid for the chosen model view. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            url (str, optional):  url endpoint for the GET :urn/metadata/:guid.
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        url = url.replace(':urn', urn.decode('utf8'))

        url = url.replace(':guid', guid)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})
        if x_ads_force in ['true', 'false']:
            headers.update({'x-ads-force' : x_ads_force})

        resp = requests.request('GET',
                                url,
                                headers=headers)

        while resp.status_code == 202:
            resp = requests.request('GET',
                                    url,
                                    headers=headers)

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content))

    def get_object_properties(self, token=None, urn=None, guid=None, accept_encoding=None, x_ads_force='true',
                              object_id=None,
                              url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid/properties'):
        """
        Send a GET :urn/metadata/:guid/properties request to the BIM360 API, returns all object properties for the given metadata id (corresponding to a model view) for the model.

        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            guid (str, optional): The guid for the chosen model view. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            object_id (str, optional): Specific Object id for which the properties are to be found. Defaults to True.
            url (str, optional):  url endpoint for the GET :urn/metadata/:guid/properties.
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/:urn/metadata/:guid/properties'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        url = url.replace(':urn', urn.decode('utf8'))

        url = url.replace(':guid', guid)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})
        if x_ads_force in ['true', 'false']:
            headers.update({'x-ads-force' : x_ads_force})

        params = {}

        if object_id is not None:
            if isinstance(object_id, (int, str)):
                params.update({'objectid' : object_id})

        resp = requests.request('GET',
                                url,
                                headers=headers,
                                params=params)

        while resp.status_code == 202:
            resp = requests.request('GET',
                                    url,
                                    headers=headers,
                                    params=params)

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content))