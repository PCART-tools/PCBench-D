def StopImmediate():
    """Stops an immediate mode run."""
    # Phew, that was a dangerous ride.
    global _immediate_mode
    global _immediate_root_folder
    if not IsImmediate():
        return
    with WorkspaceGuard(_immediate_workspace_name):
        ResetWorkspace()
    shutil.rmtree(_immediate_root_folder)
    _immediate_root_folder = ''
    _immediate_mode = False
