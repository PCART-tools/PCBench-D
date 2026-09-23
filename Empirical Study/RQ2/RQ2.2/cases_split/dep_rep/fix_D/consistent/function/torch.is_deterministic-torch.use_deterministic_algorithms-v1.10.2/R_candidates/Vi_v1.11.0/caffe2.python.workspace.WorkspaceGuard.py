@contextlib.contextmanager
def WorkspaceGuard(workspace_name):
    current = CurrentWorkspace()
    SwitchWorkspace(workspace_name, True)
    yield
    SwitchWorkspace(current)
