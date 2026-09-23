def _handle_col_wise_sharding(input, world_size, weight, local_shard_t, bias, pg):
    # allgather the inputs first.
    gathered_inputs = [torch.zeros_like(input) for _ in range(world_size)]
    dist.all_gather(gathered_inputs, input, group=pg)

    # matmul all the inputs.
    results = []
    for i, inp in enumerate(gathered_inputs):
        results.append(inp.matmul(local_shard_t).t())

    # Process inputs and outputs for all2all.
    sharding_dim_size = weight.size()[0]
    output = torch.empty((sharding_dim_size, input.size(0)), device=input.device)
    combined_results = torch.cat(results)

    # Compute output splits
    split_size = get_split_size(sharding_dim_size, world_size)
    output_split_sizes = [
        get_chunked_dim_size(sharding_dim_size, split_size, placement.rank())
        for placement in weight._sharding_spec.placements
    ]

    # distribute the outputs using all2all.
    dist.all_to_all_single(output, combined_results, output_split_sizes=output_split_sizes, group=pg)

    # Check if we need to rearrange rows appropriately for output.
    rearrange_rows = any([idx != placement.rank() for idx, placement in enumerate(weight._sharding_spec.placements)])
    if rearrange_rows:
        indices = []
        for placement in weight._sharding_spec.placements:
            dim_size = output_split_sizes[placement.rank()]
            start = sum([split_size if i < placement.rank() else 0 for i, split_size in enumerate(output_split_sizes)])
            indices += list(range(start, start + dim_size))

        output = output.index_select(0, torch.tensor(indices, device=output.device))

    # add bias and return result.
    return output.t() + bias
