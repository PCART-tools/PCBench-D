def _init_sharded_tensor_from_local_result(
    sharded_tensor,
    local_result,
    tensor_shard_dim,
    result_shard_dim,
    world_size,
    pg,
):
    """
    Given a sharded tensor and local_result from an op on top of it. We want
    to create a new sharded tensor from the local_result so that the the next
    op can be performed on the basis of the new sharded tensor. This can seen
    as the last step of the first phase of the Megatron-LM style model(tensor)
    parallelism.

    Args:
        sharded_tensor: Sharded tensor which the op was performed on.
        local_result: A tensor which is from the op performed on the local_shard of
            the sharded_tensor.
        tensor_shard_dim: Dim which the tensor is sharded on.
        result_shard_dim: Dim which the new sharded tensor will be sharded on.
        world_size: number of ranks.
        pg (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.

    Return:
        A :class:`ShardedTensor` object which filled with local intermediate results.
    """
    sharded_weight_metadata = copy.deepcopy(sharded_tensor.local_shards()[0].metadata)
    current_offsets = [0] * local_result.dim()
    current_offsets[result_shard_dim] = sharded_weight_metadata.shard_offsets[
        tensor_shard_dim
    ]
    global_size = list(local_result.size())
    global_size[result_shard_dim] = sharded_tensor.size(tensor_shard_dim)
    local_shard_metadata = ShardMetadata(
        shard_offsets=current_offsets,
        shard_sizes=list(local_result.size()),
        placement=sharded_weight_metadata.placement,
    )
    local_shards = [Shard(local_result, local_shard_metadata)]
    new_st = ShardedTensor._init_from_local_shards(
        local_shards, tuple(global_size), process_group=pg
    )

    # Manually set sharding_spec
    new_st._sharding_spec = copy.deepcopy(sharded_tensor._sharding_spec)
    new_st._sharding_spec.dim = result_shard_dim
    return new_st
