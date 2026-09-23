def _handle_row_wise_sharding_sharded_tensor(
    input, world_size, weight, local_shard_t, bias, pg
):
    """
    Entry-point function to handle the logic of row-wise sharding of weight
    for Linear when the input is a sharded tensor. (Detailed explanations
    of the logic can be found in the comment for sharded_linear.)

    Args:
        input: matrix to be multiplied with the sharded weight.
        world_size: number of ranks.
        weight: shareded weight tensor.
        local_shard_t: row-wise shared local weight used for lookup.
        bias: bias term of linear op.
        pg: process group.

    Returns:
        A :class:`_PartialTensor` object which stores the partial local result.
    """
    results = []
    local_shard = input.local_shards()[0].tensor
    indices = [0] * world_size
    reaggrance_partial = False
    for idx, placement in enumerate(input._sharding_spec.placements):
        indices[placement.rank()] = idx
        if idx != placement.rank():
            reaggrance_partial = True

    for tensor in torch.tensor_split(local_shard, world_size):
        results.append(
            tensor.matmul(local_shard_t) + _BiasTensorPartial.apply(world_size, bias)
        )
    if reaggrance_partial:
        results = [results[idx] for idx in indices]

    # Return the partial local result.
    return _PartialTensor(torch.cat(results), pg)
