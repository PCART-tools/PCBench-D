def _shard_tensor(
    tensor: torch.Tensor, sharding_spec: ShardingSpec, src_rank=0, process_group=None
) -> ShardedTensor:
    """
    Given a :class:`torch.Tensor`, it shards that tensor according to the provided
    ``sharding_spec``. ``src_rank`` denotes the source rank which would be
    used as the ground truth of the data which would be scattered as shards
    across the rest of the ranks.

    Args:
        tensor (:class:`torch.Tensor`): Tensor needs to be sharded.
        sharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.

    Keyword args:
        src_rank (int, optional): The source rank which is used as the ground truth of
            the data for the parameter that would be sharded and scattered
            across the rest of the ranks.
            Default: 0.
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.

    Returns:
        A :class:`ShardedTensor` sharded from the given tensor.

    .. warning::
        Only :class:`torch.distributed._shard.sharding_spec.ChunkShardingSpec` is
        currently supported as the ``sharding_spec``.
    """
    if not tensor.is_contiguous():
        raise ValueError("input tensor is not a contiguous Tensor")

    pg = (
        process_group
        if process_group is not None
        else distributed_c10d._get_default_group()
    )
    world_size = dist.get_world_size(pg)
    current_rank = dist.get_rank(pg)

    # Validate src_rank and sharding_spec are same across all ranks.
    gathered_list = [None] * world_size
    dist.all_gather_object(gathered_list, (src_rank, sharding_spec), group=pg)

    for idx, entry in enumerate(gathered_list):
        if src_rank != entry[0]:  # type: ignore[index]
            raise ValueError(
                f"src_rank={src_rank} on rank: {current_rank} does not "  # type: ignore[index]
                f"match with src_rank={entry[0]} on rank: {idx}"  # type: ignore[index]
            )
        if sharding_spec != entry[1]:  # type: ignore[index]
            raise ValueError(
                f"sharding_spec={sharding_spec} on rank: {current_rank} does not "  # type: ignore[index]
                f"match with sharding_spec={entry[1]} on rank: {idx}"  # type: ignore[index]
            )

    st = sharding_spec.shard(tensor, src_rank=src_rank, process_group=pg)

    return st
