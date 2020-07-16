# -*- coding: utf-8 -*-
"""Module containing classes related to deriving model data from the Autodesk Forge BIM360 platform."""
import requests
from urllib3.util.retry import Retry
from requests_toolbelt import sessions
import base64
from urllib.parse import quote_plus
from PyForge.TimeoutHttpAdapter import TimeoutHttpAdapter

class ModelDerivativeApi():
    """This class provides the base API calls for Autodesk BIM360 model derivatives."""

    def __init__(self, token, 
                 base_url=r'https://developer.api.autodesk.com/modelderivative/v2/designdata/',
                 timeout=1):
        """
        Initialize the ModelDerivativeApi class and optionally attach an authentication token for the Autodesk Forge API.

        Args:
            token (str): Authentication token for Autodesk Forge API.
            base_url (str, optional): Base URL for calls to the model derivative API. 
                Defaults to r'https://developer.api.autodesk.com/modelderivative/v2/designdata/'
            timeout (float, optional): Default timeout for API calls. Defaults to 0.1.

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

    def get_manifest(self, urn=None, accept_encoding=None, endpoint=r':urn/manifest'):
        """
        Send a GET :urn/metadata request to the BIM360 API, returns information about derivatives that correspond to a specific source file, including derivative URNs and statuses.

        Args:
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            endpoint (str, optional):  endpoint for the GET :urn/metadata. Defaults to r':urn/manifest'

        Raises:
            ValueError: If any of token and self.token, urn are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ModelDerivativeApi.")

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        endpoint = endpoint.replace(':urn', urn.decode('utf8'))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_derivative(self, urn=None, derivative_urn=None, endpoint=r':urn/manifest/:derivativeUrn'):
        """
        Send a GET  :urn/manifest/:derivativeurn request to the BIM360 API, Downloads a selected derivative.

        Args:
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            derivative_urn (str, optional): The urn for the chosen derivative. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            endpoint (str, optional):  endpoint for the GET /:urn/metadata/:guid. Defaults to r':urn/manifest/:derivativeUrn'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ModelDerivativeApi.")

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        endpoint = endpoint.replace(':urn', urn.decode('utf8'))

        endpoint = endpoint.replace(':derivativeUrn', quote_plus(derivative_urn))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

        resp = self.http.get(endpoint, headers=headers)

        while resp.status_code == 202:
            resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            return resp

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_metadata_ids(self, urn=None, accept_encoding=None, endpoint=r':urn/metadata'):
        """
        Send a GET :urn/metadata request to the BIM360 API, returns the available metadata ID's for the model.

        Args:
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            endpoint (str, optional):  endpoint for the GET :urn/metadata. Defaults to r':urn/metadata'

        Raises:
            ValueError: If any of token and self.token, urn are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ModelDerivativeApi.")

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        endpoint = endpoint.replace(':urn', urn.decode('utf8'))

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_object_tree(self, urn=None, guid=None, accept_encoding=None, x_ads_force='true', endpoint=r':urn/metadata/:guid'):
        """
        Send a GET :urn/metadata/:guid request to the BIM360 API, returns the object tree for the given metadata id (corresponding to a model view) for the model.

        Args:
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            guid (str, optional): The guid for the chosen model view. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            endpoint (str, optional): Endpoint for the GET :urn/metadata/:guid. Defaults to r':urn/metadata/:guid'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ModelDerivativeApi.")

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        endpoint = endpoint.replace(':urn', urn.decode('utf8'))

        endpoint = endpoint.replace(':guid', guid)

        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        if accept_encoding is not None:
            if accept_encoding in ['*', 'gzip']:
                headers.update({'Accept-Encoding' : accept_encoding})
        if x_ads_force in ['true', 'false']:
            headers.update({'x-ads-force' : x_ads_force})

        resp = self.http.get(endpoint, headers=headers)

        while resp.status_code == 202:
            resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_object_properties(self, urn=None, guid=None, accept_encoding=None, x_ads_force='true',
                              object_id=None, endpoint=r':urn/metadata/:guid/properties'):
        """
        Send a GET :urn/metadata/:guid/properties request to the BIM360 API, returns all object properties for the given metadata id (corresponding to a model view) for the model.

        Args:
            urn (str, optional): The urn for the BIM360 model. Defaults to None.
            guid (str, optional): The guid for the chosen model view. Defaults to None.
            accept_encoding (str, optional): Specifies if the results may be compressed (allowed: gzip or *). Defaults to None.
            x_ads_force (str, optional): Specifies if the tree is to be force retrieved even though it failed to be retrieved or got timeout previously. Possible values [true/false]. Defaults to true.
            object_id (str, optional): Specific Object id for which the properties are to be found. Defaults to True.
            endpoint (str, optional): Endpoint for the GET :urn/metadata/:guid/properties. Defaults to r':urn/metadata/:guid/properties'

        Raises:
            ValueError: If any of token and self.token, urn and guid are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.

        Returns:
            None.
        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the ModelDerivativeApi.")

        if urn is None:
            raise ValueError("Please enter an urn.")

        urn = base64.urlsafe_b64encode(urn.encode('utf8'))

        endpoint = endpoint.replace(':urn', urn.decode('utf8'))

        endpoint = endpoint.replace(':guid', guid)

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

        resp = self.http.get(endpoint, headers=headers, params=params)

        while resp.status_code == 202:
            resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            return resp.json()['data']

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))