def validate_non_overlapping_shards_metadata(shards: List[ShardMetadata]):
    """
    Ensures none of the shards overlap with each other.

    Args:
        shards(List[ShardMetadata]): List of :class:`ShardMetadata` objects representing
            each shard.
    Raises:
        ``ValueError`` if there's overlap in any two shards.
    """
    # TODO: evaluate optimizing this if needed.
    for i in range(len(shards)):
        for j in range(i + 1, len(shards)):
            if _check_shard_metadata_pair_overlap(shards[i], shards[j]):
                raise ValueError(f'Shards {shards[i]} and {shards[j]} overlap')
