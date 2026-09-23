def _get_group_rank(group: ProcessGroup, rank):
    """
    Helper that gets a given group's local rank in the group from a given global
    rank.
    """
    if group is GroupMember.WORLD:
        raise RuntimeError(
            "group.WORLD does not have local rank to global " "rank mapping"
        )
    if group not in _pg_group_ranks:
        raise RuntimeError("The given group does not exist")
    try:
        group_rank = _pg_group_ranks[group][rank]
    except KeyError:
        raise RuntimeError(
            f"The global rank {rank} is not part of the group {group}"
        ) from None
    return group_rank
