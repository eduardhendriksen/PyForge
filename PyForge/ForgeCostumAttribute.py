# -*- coding: utf-8 -*-
"""Module containing classes related to hubs on the Autodesk Forge BIM360 platform."""
from PyForge.ForgeApi import ForgeApi
import json

class CustomAttributesApi(ForgeApi):
    """Fetch a list of custom attribute definitions that are available for specified folder."""

    def __init__(self, token, base_url=r'https://developer.api.autodesk.com/bim360/docs/v1/projects/',
                 timeout=1):
        """
        Initialize the CustomAttributeDefinitionsApi class and optionally attach an authentication token for the Autodesk Forge API.
        Args:
            token (str, optional): Authentication token for Autodesk Forge API. Defaults to None.
            base_url (str, optional): Base URL for calls to the Custom Attributes API.
                Defaults to r'https://developer.api.autodesk.com/bim360/docs/v1/projects/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.
        Returns:
            None.
        """
        
        super().__init__(token=token, base_url=base_url, timeout=timeout)

    def get_custom_attribute_definitions(self, project_id, folder_id,
                   endpoint=r':project_id/folders/:folder_id/custom-attribute-definitions'):
        """
        Send a GET :project_id/folders/:folder_id/custom-attribute-definitions request to the BIM360 API, returns the custom attribute definitions JsonApiObject available to the Autodesk account on the given hub for the given project id.
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project the folder is in.
            folder_id (str): The folder id for the folder.
            endpoint (str): endpoint for the GET :project_id/folders/:folder_id/custom-attribute-definitions request.
                Defaults to r':project_id/folders/:folder_id/custom-attribute-definitions'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): List of custom-attribute-definitions JsonApi  object in the form of a dict.
        """
        method = 'GET'

        if (self.token is None and token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if project_id.startswith("b."):
            project_id = project_id[2:]

        if folder_id is None:
            raise ValueError("Please enter a folder id.")

        
        endpoint = endpoint.replace(':project_id', project_id).replace(':folder_id', folder_id)
        
        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})

       

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            cont = resp.json()
            return cont
        
        if resp.status_code == 400:
            raise ConnectionError(resp.content)

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")  
        
        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))


    def post_version_batch_get(self, project_id, urns,
                   endpoint=r':project_id/versions:batch-get'):
        """
        Send a POST :project_id/versions:batch-get request to the BIM360 API, returns the version batch JsonApiObject available to the Autodesk account on the given hub for the given project id.
        Args:
            token (str): Authentication token for Autodesk Forge API.
            project_id (str): The project id for the project 
            endpoint (str): endpoint for the POST :project_id/versions:batch-get
                Defaults to r':project_id/versions:batch-get'.
        Raises:
            ValueError: If any of token and self.token, project_id or folder_id are of NoneType.
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors from the Forge API.
        Returns:
            dict(JsonApiObject): List of versions batch JsonApi  object in the form of a dict.
        """
        method = 'POST'

        if (self.token is None):
            raise ValueError("Please give a authorization token.")

        if self.token is not None:
            token = self.token

        if project_id is None:
            raise ValueError("Please enter a project id.")

        if project_id.startswith("b."):
            project_id = project_id[2:]
 
                
        endpoint = endpoint.replace(':project_id', project_id)
        
        headers = {}

        headers.update({'Authorization' : "Bearer {}".format(token)})
        
        headers.update({'Content-Type' : 'application/json'})
        
        data = {}
        
        data.update({"urns" : urns})
        
        data = json.dumps(data)            

        resp = self.http.post(endpoint, headers=headers, data=data)

        if resp.status_code == 200:
            cont = resp.json()
            return cont
        
        if resp.status_code == 400:
            raise ConnectionError(resp.content)

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")  
        
        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))
        



