def get_process_group_ranks(group: ProcessGroup) -> list[int]:
    """
    Get all ranks associated with ``group``.

    Args:
        group (ProcessGroup): ProcessGroup to get all ranks from.

    Returns:
        List of global ranks ordered by group rank.
    """
    return list(_world.pg_group_ranks[group].keys())
