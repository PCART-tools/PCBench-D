def _handle_col_wise_sharding(input, world_size, weight, rank, local_shard_t, bias, pg):
    """
    Entry-point function to handle the logic of col-wise sharding of weight
    for Linear. (Detailed explanations of the logic can be found in the
    comment for sharded_linear.)

    When the local tensor only has one dimension, we increase one more dimension
    for reshard. We need to do squeeze manually to reduce the dimension later-on.

    For example, if we have:
    input: size[15]
    weight: size[15, 16]
    world_size: 4

    In each rank, we will have 4 * [4] tensors. We then stack them into a [4, 4]
    tensor and generate a sharded tenor sharded by dim 1.

    For the rest situations, we just simply concatenate local tensors. No more actions
    are needed afterward.

    Args:
        input: matrix to be multiplied with the sharded weight.
        world_size: number of ranks.
        weight: shareded weight tensor.
        rank: # of cuda process.
        local_shard_t: row-wise shared local weight used for lookup.
        bias: bias term of linear op.
        pg: process group.

    Returns:
        A :class:`ShardedTensor` object which filled with local intermediate results.
    """
    # allgather the inputs first.
    gathered_inputs = all_gather(input, group=pg)
    (start_pos, chunk_size) = get_chunk_sharding_params(
        bias.size(0), world_size, weight._sharding_spec, rank
    )
    local_bias = _BiasTensorNarrow.apply(
        world_size, start_pos, chunk_size, weight, pg, bias
    )
    results = [None] * world_size
    indices = {}
    for idx, placement in enumerate(weight._sharding_spec.placements):
        indices[placement.rank()] = idx
    for i, inp in enumerate(gathered_inputs):
        results[indices[i]] = inp.matmul(local_shard_t) + local_bias
    # When the local result only has one dimension, we need to make sure
    # it does not shard by dim 0. So reshard can work properly.
    if results[0].dim() == 1:  # type: ignore[attr-defined]
        result = torch.stack(results)  # type: ignore[arg-type]
    else:
        result = torch.cat(results)  # type: ignore[arg-type]
    return _init_sharded_tensor_from_local_result(
        weight, result, 0, -1, world_size, pg  # type: ignore[arg-type]
    )
