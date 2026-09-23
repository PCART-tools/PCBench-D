def get_backend(group: Optional[ProcessGroup] = None) -> Backend:
    """
    Return the backend of the given process group.

    Args:
        group (ProcessGroup, optional): The process group to work on. The
            default is the general main process group. If another specific group
            is specified, the calling process must be part of :attr:`group`.

    Returns:
        The backend of the given process group as a lower case string.

    """
    pg = group or _get_default_group()
    if _rank_not_in_group(pg):
        raise ValueError("Invalid process group specified")

    pg_store = _world.pg_map.get(pg, None)
    if pg_store is None:
        raise ValueError(
            f"Process group {pg} is not initialized in the world group map. Please initialize the group first."
        )

    return Backend(not_none(pg_store)[0])
