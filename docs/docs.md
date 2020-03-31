---
description: |
    API documentation for modules: PyForge, PyForge.AuthNegotiator, PyForge.FolderTree, PyForge.ForgeBusinessUnits, PyForge.ForgeCompanies, PyForge.ForgeFolders, PyForge.ForgeHubs, PyForge.ForgeProjects, PyForge.ForgeUsers, PyForge.ForgeVersions.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...



# Module `PyForge` {#PyForge}

Python tools to communicate with the Autodesk Forge Api.




## Sub-modules

* [PyForge.AuthNegotiator](#PyForge.AuthNegotiator)
* [PyForge.FolderTree](#PyForge.FolderTree)
* [PyForge.ForgeBusinessUnits](#PyForge.ForgeBusinessUnits)
* [PyForge.ForgeCompanies](#PyForge.ForgeCompanies)
* [PyForge.ForgeFolders](#PyForge.ForgeFolders)
* [PyForge.ForgeHubs](#PyForge.ForgeHubs)
* [PyForge.ForgeProjects](#PyForge.ForgeProjects)
* [PyForge.ForgeUsers](#PyForge.ForgeUsers)
* [PyForge.ForgeVersions](#PyForge.ForgeVersions)







# Module `PyForge.AuthNegotiator` {#PyForge.AuthNegotiator}

Module containing classes related to authentication on the Autodesk Forge BIM360 platform.







## Classes



### Class `OAuth2Negotiator` {#PyForge.AuthNegotiator.OAuth2Negotiator}



> `class OAuth2Negotiator(webAddress, clientId, clientSecret, scopes, redirectAddress=None, endAddress=None)`


Class to negotiate the authentication with the Autodesk Forge Api Authentication servers.

Initialize the OAuth2Negotiator class and assign the needed parameters for authentication.


#### Args

**`webAddress`** :&ensp;`str`
:   Web address for the Autodesk Forge API authentication server.


**`clientId`** :&ensp;`str`
:   Client id for the Forge App this authentication is used for.


**`clientSecret`** :&ensp;`str`
:   Client secret for the Forge App this authentication is used for.


**`scopes`** :&ensp;`list`, `str`
:   API access scopes requested in the authentication.


**`redirectAddress`** :&ensp;`str`, optional
:   Redirect web address used for 3-legged authentication. Defaults to None.


**`endAddress`** :&ensp;`str`, optional
:   End web address to redirect to after 3-legged authentication has succeeded. Defaults to None.



#### Raises

**`TypeError`**
:   If the type of the scopes argument is not list of str this error is raised.



#### Returns

None.









#### Methods



##### Method `get_token` {#PyForge.AuthNegotiator.OAuth2Negotiator.get_token}




> `def get_token(self, legs=2)`


Contact the Autodesk Forge API Authentication server and obtain an access token.


###### Args

**`legs`** :&ensp;`int`, optional
:   Indicates if 2- or 3-legged authentication is used. Defaults to 2.



###### Raises

**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

**`str`**
:   Autodesk Forge acces token.


**`int`**
:   Time in s that the token stays active.






# Module `PyForge.FolderTree` {#PyForge.FolderTree}

Module containing classes to implementing and navigating data structures from Autodesk Forge BIM360 platform.







## Classes



### Class `FolderTree` {#PyForge.FolderTree.FolderTree}



> `class FolderTree(folder, parent=None, children=None)`


This class sets up a simple folder tree with children and parent folders linked to the BIM360 API.

Initialize a FolderTree instance with a given BIM360 Api folder object and potentially attaches the parent and the folders children.


#### Args

folder (dict(JsonApiObject)): The BIM360 Api folder object this instance is linked to in the form of a dict.
**`parent`** :&ensp;[`FolderTree`](#PyForge.FolderTree.FolderTree), optional
:   The FolderTree object that is this instance's parent. Defaults to None.


children (list(FolderTree), optional): List of FolderTree objects that are this instance's children. Defaults to None.

#### Raises

**`ValueError`**
:   Raised if the given folder argument is of NoneType.



#### Returns

None.









#### Methods



##### Method `get_children` {#PyForge.FolderTree.FolderTree.get_children}




> `def get_children(self, token, project_id)`


Get the children folder JsonApi objects of this FolderTree instance in the form of a list of dicts.


###### Args

**`token`** :&ensp;`str`
:   Authentication token for Autodesk Forge API.


**`project_id`** :&ensp;`str`
:   The project id for the project the folder is in.



###### Raises

**`ValueError`**
:   Is raised if token or project_id are NoneType.



###### Returns

`children_folders` (`list`(`dict`(`JsonApiObject`))): `Children` `folders` of `this` [`FolderTree`](#PyForge.FolderTree.FolderTree) `instance` `in` `the` `form` of `a` `list` of `dicts`
:   &nbsp;


containing JsonApiObjects.



##### Method `populate` {#PyForge.FolderTree.FolderTree.populate}




> `def populate(self, token, project_id)`


Populate this FolderTree instance recursively down all of its' children in the Autodesk BIM360 folder structure.


###### Args

**`token`** :&ensp;`str`
:   Authentication token for Autodesk Forge API.


**`project_id`** :&ensp;`str`
:   The project id for the project the folder is in.



###### Returns

None.



##### Method `search_tree` {#PyForge.FolderTree.FolderTree.search_tree}




> `def search_tree(self, folder_name)`


Search the for the FolderTree instance with the given name in this FolderTree's children, recursively.


###### Args

**`folder_name`** :&ensp;`str`
:   The name of the Autodesk BIM360 folder to be searched for.



###### Returns

**[`FolderTree`](#PyForge.FolderTree.FolderTree)**
:   FolderTree instance with the given name.






# Module `PyForge.ForgeBusinessUnits` {#PyForge.ForgeBusinessUnits}

Module containing classes related to business units on the Autodesk Forge BIM360 platform.







## Classes



### Class `BusinessUnitsApi` {#PyForge.ForgeBusinessUnits.BusinessUnitsApi}



> `class BusinessUnitsApi(token=None)`


This class provides the base API calls for Autodesk BIM360 business units.

Initialize the BusinessUnitsApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_account_business_units` {#PyForge.ForgeBusinessUnits.BusinessUnitsApi.get_account_business_units}




> `def get_account_business_units(self, token=None, account_id=None, url=' https://developer.api.autodesk.com/hq/v1/accounts/:account_id/business_units_structure')`


Send a GET accounts/:account_id/business_units_structure request to the BIM360 API, returns the business units available to the Autodesk account on the given account.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`account_id`** :&ensp;`str`, optional
:   The account id for the BIM360 account. Defaults to None.


**`limit`** :&ensp;`int`, optional
:   Size of the response array. Defaults to 100.


**`offset`** :&ensp;`int`, optional
:   Offset of the response array. Defaults to 0.


**`sort`** :&ensp;`list`, optional
:   List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].


**`field`** :&ensp;`list`, optional
:   List of string field names to include in the response array. Defaults to [].


**`url`** :&ensp;`str`, optional
:    url endpoint for the GET accounts/:account_id/business units request.
    Currently default is pointed at the US BIM360 servers.
    EMEA server:   <https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/business_units_structure>
    Defaults to  <https://developer.api.autodesk.com/hq/v1/accounts/:account_id/business_units_structure.>



###### Raises

**`ValueError`**
:   If any of token and self.token, account_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

None.





# Module `PyForge.ForgeCompanies` {#PyForge.ForgeCompanies}

Module containing classes related to companies on the Autodesk Forge BIM360 platform.







## Classes



### Class `CompaniesApi` {#PyForge.ForgeCompanies.CompaniesApi}



> `class CompaniesApi(token=None)`


This class provides the base API calls for Autodesk BIM360 companies.

Initialize the CompaniesApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_account_companies` {#PyForge.ForgeCompanies.CompaniesApi.get_account_companies}




> `def get_account_companies(self, token=None, account_id=None, limit=100, offset=0, sort=[], field=[], url='https://developer.api.autodesk.com/hq/v1/accounts/:account_id/companies')`


Send a GET accounts/:account_id/companies request to the BIM360 API, returns the companies available to the Autodesk account on the given account.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`account_id`** :&ensp;`str`, optional
:   The account id for the BIM360 account. Defaults to None.


**`limit`** :&ensp;`int`, optional
:   Size of the response array. Defaults to 100.


**`offset`** :&ensp;`int`, optional
:   Offset of the response array. Defaults to 0.


**`sort`** :&ensp;`list`, optional
:   List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].


**`field`** :&ensp;`list`, optional
:   List of string field names to include in the response array. Defaults to [].


**`url`** :&ensp;`str`, optional
:    url endpoint for the GET accounts/:account_id/companies request.
    Currently default is pointed at the US BIM360 servers.
    EMEA server:  <https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/companies>
    Defaults to <https://developer.api.autodesk.com/hq/v1/accounts/:account_id/companies.>



###### Raises

**`ValueError`**
:   If any of token and self.token, account_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

None.





# Module `PyForge.ForgeFolders` {#PyForge.ForgeFolders}

Module containing classes related to folders on the Autodesk Forge BIM360 platform.







## Classes



### Class `FoldersApi` {#PyForge.ForgeFolders.FoldersApi}



> `class FoldersApi(token=None)`


This class provides the base API calls for Autodesk BIM360 folders.

Initialize the FoldersApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_folder` {#PyForge.ForgeFolders.FoldersApi.get_folder}




> `def get_folder(self, token, project_id, folder_id, url='https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id')`


Send a GET projects/:project_id/folders/:folder_id request to the BIM360 API, returns the folder JsonApiObject available to the Autodesk account on the given hub for the given project id.


###### Args

**`token`** :&ensp;`str`
:   Authentication token for Autodesk Forge API.


**`project_id`** :&ensp;`str`
:   The project id for the project the folder is in.


**`folder_id`** :&ensp;`str`
:   The folder id for the folder.


**`url`** :&ensp;`str`, optional
:   url endpoint for the GET projects/:project_id/folders/:folder_id request.
    Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'.



###### Raises

**`ValueError`**
:   If any of token and self.token, project_id or folder_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

dict(JsonApiObject): JsonApi Folder object in the form of a dict.



##### Method `get_folder_contents` {#PyForge.ForgeFolders.FoldersApi.get_folder_contents}




> `def get_folder_contents(self, token=None, project_id=None, folder_id=None, type_filter=None, url='https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/contents')`


Send a GET projects/:project_id/folders/:folder_id/contents request to the BIM360 API, returns the folder contents available to the Autodesk account on the given hub.


###### Args

**`token`** :&ensp;`str`
:   Authentication token for Autodesk Forge API.


**`project_id`** :&ensp;`str`
:   The project id for the project the folder is in.


**`folder_id`** :&ensp;`str`
:   The folder id for the folder.


**`type_filter`** :&ensp;`str`, `list`
:   BIM360 item type or list of BIM360 item types to filter for.


**`url`** :&ensp;`str`
:   url endpoint for the GET projects/:project_id/folders/:folder_id/contents request.
    Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/contents'.



###### Raises

**`ValueError`**
:   If any of token and self.token, project_id or folder_id are NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

list(dict(JsonApiObject)): List of JsonApi Data objects in the form of dicts.
list(dict(JsonApiObject)): List of JsonApi Version objects in the form of dicts.



##### Method `make_filter_param` {#PyForge.ForgeFolders.FoldersApi.make_filter_param}




> `def make_filter_param(self, filter_entries, filter_type)`


Create a filter query parameter of the given type with the given entries.


###### Args

**`filter_entries`** :&ensp;`str`, `list`
:   The entries to be filtered for.


**`filter_type`** :&ensp;`str`
:   The type of filter to be made.



###### Raises

**`TypeError`**
:   Raised if the filter_entries parameter is not of type str or list.



###### Returns

**`dict`**
:   A filter dictionary to be used as a query parameter.




##### Method `search_folder` {#PyForge.ForgeFolders.FoldersApi.search_folder}




> `def search_folder(self, token, project_id, folder_id, search_filter, type_filter, url='https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id')`


Send a GET projects/:project_id/folders/:folder_id/search request to the BIM360 API, recursively searching the folder and subfolders for the given search filter. Returns the search results data JsonApi Objects available to the user in the given search.


###### Args

**`token`** :&ensp;`str`
:   Authentication token for Autodesk Forge API. Must be 3-legged with data:search scope requested.


**`project_id`** :&ensp;`str`
:   The project id for the project the folder to be searched is in.


**`folder_id`** :&ensp;`str`
:   The folder id for the folder to be searched.


**`search_filter`** :&ensp;`str`, `list`
:   The filter(s) to search for.


**`type_filter`** :&ensp;`str`, `list`
:   Autodesk item type filter(s).


**`url`** :&ensp;`TYPE`, optional
:   Url endpoint for the GET projects/:project_id/folders/:folder_id request.
    Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id'.



###### Raises

**`ValueError`**
:   If any of token and self.token, project_id or folder_id are NoneType.


**`TypeError`**
:   If search filter is of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

list(dict(JsonApiObject)): List of JsonApi Data objects in the form of dicts.
list(dict(JsonApiObject)): List of JsonApi Version objects in the form of dicts.





# Module `PyForge.ForgeHubs` {#PyForge.ForgeHubs}

Module containing classes related to hubs on the Autodesk Forge BIM360 platform.







## Classes



### Class `HubsApi` {#PyForge.ForgeHubs.HubsApi}



> `class HubsApi(token=None)`


This class provides the base API calls for Autodesk BIM360 hubs.

Initialize the HubsApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_hubs` {#PyForge.ForgeHubs.HubsApi.get_hubs}




> `def get_hubs(self, token=None, url='https://developer.api.autodesk.com/project/v1/hubs')`


Send a GET hubs request to the BIM360 API, returns the hubs available to the Autodesk account.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`url`** :&ensp;`str`, optional
:   Url endpoint for the GET hubs request. Defaults to r'https://developer.api.autodesk.com/project/v1/hubs'.



###### Raises

**`ValueError`**
:   If all of token and self.token are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

list(dict(JsonApiObject)): List of hub JsonApi objects in the form of dicts.





# Module `PyForge.ForgeProjects` {#PyForge.ForgeProjects}

Module containing classes related to projects on the Autodesk Forge BIM360 platform.







## Classes



### Class `ProjectsApi` {#PyForge.ForgeProjects.ProjectsApi}



> `class ProjectsApi(token=None)`


This class provides the base API calls for Autodesk BIM360 projects.

Initialize the ProjectsApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_account_projects` {#PyForge.ForgeProjects.ProjectsApi.get_account_projects}




> `def get_account_projects(self, token=None, account_id=None, limit=100, offset=0, sort=[], field=[], url='https://developer.api.autodesk.com/hq/v1/accounts/:account_id/projects')`


Send a GET accounts/:account_id/projects request to the BIM360 API, returns the projects available to the Autodesk account on the given account.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`account_id`** :&ensp;`str`, optional
:   The account id for the BIM360 account. Defaults to None.


**`limit`** :&ensp;`int`, optional
:   Size of the response array. Defaults to 100.


**`offset`** :&ensp;`int`, optional
:   Offset of the response array. Defaults to 0.


**`sort`** :&ensp;`list`, optional
:   List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].


**`field`** :&ensp;`list`, optional
:   List of string field names to include in the response array. Defaults to [].


**`url`** :&ensp;`str`, optional
:    url endpoint for the GET accounts/:account_id/projects request.
    Currently default is pointed at the US BIM360 servers.
    EMEA server: <https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/projects>
    Defaults to <https://developer.api.autodesk.com/hq/v1/accounts/:account_id/projects.>



###### Raises

**`ValueError`**
:   If any of token and self.token, account_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

None.



##### Method `get_hub_projects` {#PyForge.ForgeProjects.ProjectsApi.get_hub_projects}




> `def get_hub_projects(self, token=None, hub_id=None, url='https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects')`


Send a GET hubs/:hub_id/projects request to the BIM360 API, returns the projects available to the Autodesk account on the given hub.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`hub_id`** :&ensp;`str`, optional
:   The hub id for the hub. Defaults to None.


**`url`** :&ensp;`str`, optional
:   url endpoint for the GET hubs/:hub_id/projects request.
    Defaults to r'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects'.



###### Raises

**`ValueError`**
:   If any of token and self.token, hub_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

list(dict(JsonApiObject)): List of project JsonApi objects in the form of dicts.





# Module `PyForge.ForgeUsers` {#PyForge.ForgeUsers}

Module containing classes related to users on the Autodesk Forge BIM360 platform.







## Classes



### Class `UsersApi` {#PyForge.ForgeUsers.UsersApi}



> `class UsersApi(token=None)`


This class provides the base API calls for Autodesk BIM360 users.

Initialize the UsersApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_project_users` {#PyForge.ForgeUsers.UsersApi.get_project_users}




> `def get_project_users(self, token=None, project_id=None, region='US', accept_language='de', filters={}, limit=100, offset=0, sort=[], fields=[], url='https://developer.api.autodesk.com/bim360/admin/v1/projects/:projectId/users')`


Send a GET projects/:projectId/users request to the BIM360 API, returns the users assigned to the project.


###### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.


**`project_id`** :&ensp;`str`, optional
:   The project id for the BIM360 project. Defaults to None.


**`region`** :&ensp;`str`, optional
:   The BIM360 server region to be adressed, can be US or EMEA. Defaults to US.


**`accept_language`** :&ensp;`str`, optional
:   The language in which the response is to be returned. Defaults to de.


**`filters`** :&ensp;`dict`, optional
:   A dict of filters in the form {filtertype : List(str filter entries)}. Defaults to {}.


**`limit`** :&ensp;`int`, optional
:   Size of the response array. Defaults to 100.


**`offset`** :&ensp;`int`, optional
:   Offset of the response array. Defaults to 0.


**`sort`** :&ensp;`list`, optional
:   List of string field names to sort in ascending order, Prepending a field with - sorts in descending order. Defaults to [].


**`fields`** :&ensp;`list`, optional
:   List of string field names to include in the response array. Defaults to [].


**`url`** :&ensp;`str`, optional
:    url endpoint for the GET projects/:projectId/users request.
    Defaults to r'https://developer.api.autodesk.com/bim360/admin/v1/projects/:projectId/users'



###### Raises

**`ValueError`**
:   If any of token and self.token, project_id are of NoneType.


**`ConnectionError`**
:   Different Connectionerrors based on retrieved ApiErrors from the Forge API.



###### Returns

None.



##### Method `make_filters` {#PyForge.ForgeUsers.UsersApi.make_filters}




> `def make_filters(self, filters)`


Create a filter query parameter of the given type with the given entries.


###### Args

filters (dict, {str, filter_name : list(str, filter entires)}): The filters to be used.

###### Raises

**`ValueError`**
:   Raised if the filter entries exceed 255 characters.


**`TypeError`**
:   Raised if the filters parameter is not of type dict.



###### Returns

**`dict`**
:   A filter dictionary to be used as a query parameter.






# Module `PyForge.ForgeVersions` {#PyForge.ForgeVersions}

Module containing classes related to item versions on the Autodesk Forge BIM360 platform.







## Classes



### Class `VersionsApi` {#PyForge.ForgeVersions.VersionsApi}



> `class VersionsApi(token=None)`


This class provides the base API calls for Autodesk BIM360 versions.

Initialize the VersionsApi class and optionally attach an authentication token for the Autodesk Forge API.


#### Args

**`token`** :&ensp;`str`, optional
:   Authentication token for Autodesk Forge API. Defaults to None.



#### Returns

None.









#### Methods



##### Method `get_version` {#PyForge.ForgeVersions.VersionsApi.get_version}




> `def get_version(self, token, project_id, version_id, url='https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id')`


Send a GET projects/:project_id/versions/:version_id request to the BIM360 API, returns the version corresponding to the version id.


###### Args

**`token`**
:   Authentication token for Autodesk Forge API.


**`project_id`**
:   The project id for the project the folder is in.


**`version_id`** :&ensp;`str`
:   Version id of the version to be obtained


**`url`** :&ensp;`str`, optional
:   url endpoint for the GET projects/:project_id/versions/:version_id request.


Defaults to r'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id'.

###### Returns

dict(JsonApiObject): Version JsonApi object in the form of a dict.