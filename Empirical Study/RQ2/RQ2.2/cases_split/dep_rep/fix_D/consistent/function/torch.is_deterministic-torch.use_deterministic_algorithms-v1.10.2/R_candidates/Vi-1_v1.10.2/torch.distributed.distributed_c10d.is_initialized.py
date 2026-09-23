def is_initialized():
    """
    Checking if the default process group has been initialized
    """
    return GroupMember.WORLD is not None
