def ResetWorkspace(root_folder=None):
    if root_folder is None:
        # Reset the workspace, but keep the current root folder setting.
        return C.reset_workspace(C.root_folder())
    else:
        if not os.path.exists(root_folder):
            os.makedirs(root_folder)
        return C.reset_workspace(root_folder)
