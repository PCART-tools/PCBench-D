def _handle_row_wise_sharding(input, world_size, weight, rank, local_shard_t, bias, pg):
    # alltoall to gather all the appropriate inputs.
    input_t = input.t().contiguous()
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
        indices: List[int] = []
        for placement in weight._sharding_spec.placements:
            sharded_dim_size = get_chunked_dim_size(input_t_size[0], split_size, placement.rank())
            input_idx = placement.rank() * split_size
            indices += range(input_idx, input_idx + sharded_dim_size)

        input_t = input_t.index_select(0, torch.tensor(indices, device=input_t.device))

    gathered_input = torch.empty(input_split_sizes[rank] * world_size, input_t_size[1], device=input_t.device)

    # Perform alltoall
    dist.all_to_all_single(gathered_input, input_t, input_split_sizes=input_split_sizes, group=pg)
    gathered_input = gathered_input.t()

    # Perform local matmuls for all shards
    shard_size = local_shard_t.size()[0]
    results = []
    for r in range(world_size):
        inp = torch.narrow(gathered_input, 1, r * shard_size, shard_size)
        results.append(inp.matmul(local_shard_t))

    # Gather all the results appropriately.
    local_result = torch.empty_like(results[rank])
    dist.reduce_scatter(local_result, results, group=pg)

    # Return the appropriate local result.
    return local_result + bias
