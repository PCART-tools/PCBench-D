def ImmediateBlobs():
    with WorkspaceGuard(_immediate_workspace_name):
        return Blobs()
