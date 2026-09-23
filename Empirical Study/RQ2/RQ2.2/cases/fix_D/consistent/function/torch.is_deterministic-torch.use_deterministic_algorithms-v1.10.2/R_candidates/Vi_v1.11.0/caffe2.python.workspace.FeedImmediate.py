def FeedImmediate(*args, **kwargs):
    with WorkspaceGuard(_immediate_workspace_name):
        return FeedBlob(*args, **kwargs)
