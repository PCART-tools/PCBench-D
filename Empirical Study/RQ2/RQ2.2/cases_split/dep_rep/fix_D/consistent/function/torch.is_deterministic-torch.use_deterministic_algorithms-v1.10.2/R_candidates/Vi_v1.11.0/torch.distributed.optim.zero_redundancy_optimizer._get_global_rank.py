def _get_global_rank(group: Any, rank: int) -> int:
    r"""
    Returns the global rank for the given group and rank.
    """
    return (rank if group is dist.group.WORLD
            else dist.distributed_c10d._get_global_rank(group, rank))
