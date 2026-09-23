def FetchImmediate(*args, **kwargs):
    with WorkspaceGuard(_immediate_workspace_name):
        return FetchBlob(*args, **kwargs)
