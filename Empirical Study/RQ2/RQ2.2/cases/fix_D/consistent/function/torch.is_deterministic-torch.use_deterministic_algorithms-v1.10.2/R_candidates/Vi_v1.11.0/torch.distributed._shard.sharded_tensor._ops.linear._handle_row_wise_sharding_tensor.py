def _handle_row_wise_sharding_tensor(
    input, world_size, weight, rank, local_shard_t, bias, pg
):
    """
    Entry-point function to handle the logic of row-wise sharding of weight
    for Linear. (Detailed explanations of the logic can be found in the
    comment for sharded_linear.)

    Args:
        input: matrix to be multiplied with the sharded weight.
        world_size: number of ranks.
        weight: shareded weight tensor.
        rank: # of cuda process.
        local_shard_t: row-wise shared local weight used for lookup.
        bias: bias term of linear op.
        pg: process group.

    Returns:
        A :class:`_PartialTensor` object which stores the partial local result.
    """
    # alltoall to gather all the appropriate inputs.
    input_t = input.transpose(0, -1).contiguous()
    input_t_size = input_t.size()

    # Compute expected size
    split_size = get_split_size(input_t_size[0], world_size)
    input_split_sizes = [0] * world_size
    rearrange_rows = False

    for idx, placement in enumerate(weight._sharding_spec.placements):
        sharded_dim_size = get_chunked_dim_size(input_t_size[0], split_size, idx)
        input_split_sizes[placement.rank()] = sharded_dim_size
        if placement.rank() != idx:
            rearrange_rows = True

    if rearrange_rows:
        # Need to re-arrange rows of input_t for all2all.
        indices: List[List[int]] = [[0]] * world_size
        # When we do the chunk split, we always ensure the first N - 1 chunks get max out
        # and then the Nth chunk gets the rest. So input_split_sizes like [3, 3, 3, 4]
        # are not possible. The expected split size will be [4, 4, 4, 1].
        sharded_dim_size_max = max(input_split_sizes)
        for idx, placement in enumerate(weight._sharding_spec.placements):
            split_size = input_split_sizes[placement.rank()]
            offset_start_idx = idx * sharded_dim_size_max
            indices[placement.rank()] = list(
                range(offset_start_idx, offset_start_idx + split_size)
            )
        indices_flatten = list(idx for indice in indices for idx in indice)

        input_t = input_t.index_select(
            0, torch.tensor(indices_flatten, device=input_t.device)
        )

    gathered_input_size = [input_split_sizes[rank] * world_size] + list(
        input_t_size[1:]
    )
    gathered_input = torch.empty(gathered_input_size, device=input_t.device)

    # Perform autograd enabled alltoall
    all_to_all_single(
        gathered_input, input_t, input_split_sizes=input_split_sizes, group=pg
    )
    gathered_input = gathered_input.transpose(0, -1)

    # Perform local matmuls for all shards
    results = []
    shard_size = local_shard_t.size()[0]
    for r in range(world_size):
        inp = torch.narrow(gathered_input, -1, r * shard_size, shard_size)
        results.append(
            inp.matmul(local_shard_t) + _BiasTensorPartial.apply(world_size, bias)
        )

    # Return the partial local result.
    return _PartialTensor(torch.cat(results), pg)
