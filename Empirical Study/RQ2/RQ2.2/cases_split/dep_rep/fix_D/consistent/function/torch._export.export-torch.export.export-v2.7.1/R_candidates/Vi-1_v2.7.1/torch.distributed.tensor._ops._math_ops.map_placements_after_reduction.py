def map_placements_after_reduction(
    placements: tuple[Placement, ...],
    reduction_dims: list[int],
    reduction_dims_map: list[int],
    reduction_op: ReductionOpType,
) -> tuple[Placement, ...]:
    """
    Map each placement based on the output shape after reduction.
    """
    new_placements: list[Placement] = []
    for placement in placements:
        if isinstance(placement, (Replicate, Partial)):
            new_placements.append(placement)
        else:
            assert isinstance(placement, Shard)
            shard_dim = placement.dim
            new_shard_dim = reduction_dims_map[shard_dim]
            if new_shard_dim == -1 or shard_dim in reduction_dims:
                # if new_shard_dim collapsed or its in the reduction dims
                # (i.e. for the case where keepdims=True), we generate partial
                new_placements.append(get_placement_from_reduction_op(reduction_op))
            else:
                new_placements.append(Shard(new_shard_dim))
    return tuple(new_placements)
