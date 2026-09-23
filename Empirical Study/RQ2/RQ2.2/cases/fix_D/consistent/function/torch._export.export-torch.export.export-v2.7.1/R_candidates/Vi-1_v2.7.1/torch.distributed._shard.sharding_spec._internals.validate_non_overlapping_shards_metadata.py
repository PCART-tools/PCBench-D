def validate_non_overlapping_shards_metadata(shards: list[ShardMetadata]):
    """
    Ensures none of the shards overlap with each other.

    Args:
        shards(List[ShardMetadata]): List of :class:`ShardMetadata` objects representing
            each shard.
    Raises:
        ``ValueError`` if there's overlap in any two shards.
    """
    if not shards or len(shards) == 1:
        return

    sharded_dims: list[int] = []
    for dim in range(len(shards[0].shard_offsets)):
        for i in range(1, len(shards)):
            if (
                shards[i].shard_offsets[dim] != shards[0].shard_offsets[dim]
                or shards[i].shard_sizes[dim] != shards[0].shard_sizes[dim]
            ):
                sharded_dims.append(dim)
                break

    pair: Optional[tuple[int, int]] = None
    if len(sharded_dims) == 0:
        # All shards are the same, all dims are not partitioned. Choose any 2.
        pair = (0, 1)
    elif len(sharded_dims) == 1:
        # Shards are partitioned over only one dimension. Overlap can be found
        # using a O(nlogn) overlapping interval algorithm.
        pair = _find_1d_overlapping_shards(shards, sharded_dims[0])
    else:
        # Shards are partitioned over more than one dimension. Fall back to
        # pair-wise check. Even though O(nlogn) algorithms (line sweep) exist
        # for 2D overlap, the implementation is not trivial and may not justify
        # the time saving in most cases.
        pair = _find_nd_overlapping_shards(shards, sharded_dims)

    if pair:
        raise ValueError(f"Shards {shards[pair[0]]} and {shards[pair[1]]} overlap")
