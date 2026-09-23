def partitioned_sharding_spec(num_partitions: int,
                              partitions: Optional[Sequence[int]],
                              aval) -> ShardingSpec:
  if partitions is None:
    maybe_replicate = () if num_partitions == 1 else (Replicated(num_partitions),)
    return ShardingSpec(
        sharding=[_UNSHARDED_INSTANCE] * len(aval.shape),
        mesh_mapping=maybe_replicate)
  else:
    assert len(partitions) == len(aval.shape)
    return ShardingSpec(
        # Chunked expects a list of integers
        sharding=map(Chunked, [[x] for x in partitions]),
        mesh_mapping=map(ShardedAxis, range(len(partitions))))
