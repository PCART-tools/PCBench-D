def _get_default_group():
    """
    Getting the default process group created by init_process_group
    """
    if not is_initialized():
        raise RuntimeError(
            "Default process group has not been initialized, "
            "please make sure to call init_process_group."
        )
    return GroupMember.WORLD
