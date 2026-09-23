def RunOperatorImmediate(op):
    with WorkspaceGuard(_immediate_workspace_name):
        RunOperatorOnce(op)
