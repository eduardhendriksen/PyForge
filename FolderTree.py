# -*- coding: utf-8 -*-


from ForgeFolders import FoldersApi


class FolderTree():
    """
    This class sets up a simple folder tree with children and parent folders linked to the BIM360 API.
    """

    def __init__(self, folder, parent=None, children=None):
        """
        Initializes a FolderTree instance with a given BIM360 Api folder object and potentially attaches the parent and the folders
        children.

        Args:
            :folder (dict(JsonApiObject)): The BIM360 Api folder object this instance is linked to in the form of a dict.
            :parent (FolderTree, optional): The FolderTree object that is this instance's parent. Defaults to None.
            :children (list(FolderTree), optional): List of FolderTree objects that are this instance's children. Defaults to None.

        Raises:
            :ValueError: Raised if the given folder argument is of NoneType.

        Returns:
            :None.

        """


        if folder is not None:
            self.folder = folder
        else:
            raise ValueError("FolderTree needs a folder object to be initialized")
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

    def get_children(self, token, project_id):
        """
        Get the children folder JsonApi objects of this FolderTree instance in the form of a list of dicts.

        Args:
            :token (str): Authentication token for Autodesk Forge API.
            :project_id (str): The project id for the project the folder is in.

        Raises:
            :ValueError: Is raised if token or project_id are NoneType.

        Returns:
            :children_folders (list(dict(JsonApiObject))): Children folders of this FolderTree instance in the form of a list of dicts
            containing JsonApiObjects.
        """

        if token is None:
            raise ValueError("Please give a authorization token.")

        if project_id is None:
            raise ValueError("Please enter a project id.")
        else:
            project_id = "b.{}".format(project_id)

        type_filter = 'folders'

        folders_api = FoldersApi(token)
        folder_data, folder_versions = folders_api.get_folder_contents(token, project_id, self.folder['id'], type_filter)

        children_folders = []

        for data in folder_data:
            children_folders.append(data)

        return children_folders

    def populate(self, token, project_id):
        """
        This method populates this FolderTree instance recursively down all of its' children in the Autodesk BIM360 folder structure.

        Args:
            :token (str): Authentication token for Autodesk Forge API.
            :project_id (str): The project id for the project the folder is in.

        Returns:
            :None.

        """

        children_list = self.get_children(token, project_id)

        for child in children_list:

            new_child = FolderTree(child, self)
            self.children.append(new_child)
            new_child.populate(token, project_id)

    def search_tree(self, folder_name):
        """
        This method allows the user to search the for the FolderTree instance with the given name in this FolderTree's children,
        recursively.

        Args:
            folder_name (str): The name of the Autodesk BIM360 folder to be searched for.

        Returns:
            FolderTree: FolderTree instance with the given name.

        """

        folder_tree = None

        for child in self.children:

            if child.folder['attributes']['name'] == folder_name:
                return child
            else:
                folder_tree = child.search_tree(folder_name)
                if folder_tree is not None:
                    return folder_tree

        return folder_tree
