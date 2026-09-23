def _find_nd_overlapping_shards(
    shards: list[ShardMetadata], sharded_dims: list[int]
) -> Optional[tuple[int, int]]:
    # Each rank has len(sharded_dims) tuples. Each tuple represent the
    # [begin, end] (inclusive) pair of that dimension.
    shard_intervals = [
        [
            (s.shard_offsets[dim], s.shard_offsets[dim] + s.shard_sizes[dim] - 1)
            for dim in sharded_dims
        ]
        for s in shards
    ]

    for i in range(len(shards)):
        shard_i = shard_intervals[i]
        for j in range(i + 1, len(shards)):
            shard_j = shard_intervals[j]
            # For each dim of each shard, check if one shard resides on the other
            # end of second shard with respect to that dim. As an example for a 2D
            # shard, we would check if one shard is above or on the left of the
            # other shard.
            overlap = True
            for interval_i, interval_j in zip(shard_i, shard_j):
                if interval_i[0] > interval_j[1] or interval_j[0] > interval_i[1]:
                    overlap = False
                    break
            if overlap:
                return (i, j)
    return None
