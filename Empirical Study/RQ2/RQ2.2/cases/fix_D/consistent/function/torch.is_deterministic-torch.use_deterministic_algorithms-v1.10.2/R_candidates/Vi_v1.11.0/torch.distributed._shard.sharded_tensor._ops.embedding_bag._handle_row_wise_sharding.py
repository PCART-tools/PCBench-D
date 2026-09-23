def _handle_row_wise_sharding(
    input,
    world_size,
    weight,
    local_shard,
    offsets,
    per_sample_weights,
    mode,
    max_norm,
    norm_type,
    padding_idx,
    rank,
    pg,
):
    """
    Entry-point function to handle the logic of row-wise sharding of weight
    for embeddingBag. (Detailed explanations of the logic can be found in
    the comment for sharded_embedding_bag.)

    Args:
        input: list of ID used for lookup and aggregation.
        world_size: number of ranks.
        weight: shareded weight tensor.
        local_shard: row-wise shared local weight used for lookup.
        offsets: list of start positions of each bag for 1D input.
        per_sample_weights: weights for weighted sum mode.
        mode: aggregation method of each bag.
        max_norm: If given, each embedding vector with norm larger
            than max_norm is renormalized to have norm max_norm.
            Note: this will modify weight in-place.
        norm_type: The p in the p-norm to compute for the max_norm option.
        padding_idx: If specified, the entries at padding_idx do
            not contribute to the gradient; therefore, the embedding
            vector at padding_idx is not updated during training,
            i.e. it remains as a fixed “pad”.
            Note that the embedding vector at padding_idx is
            excluded from the reduction.
        rank: # of cuda process.
        pg: process group.

    Returns:
        gathered_output: final result of lookup and aggregation.
    """
    # We sort each interval defined by offset. If 2D, each interval is a row.
    input_size = input.size()
    (
        input_split_sorted_list,
        input_split_sorted_indices,
        split_sizes_1d,
        split_sizes_1d_with_padding,
    ) = _input_split_sort(input, offsets, padding_idx)

    # Within each interval of the sorted list, we first need to distribute
    # each ID to different bucket(rank) and also ensure the rearrangement
    # has been done in case the placement idx not equal to rank.
    # We then perform some simple stats on each interval for the next step
    # If user specifies per_sample_weights we need to rearrange them
    # to be sync with IDs and then distribute them to each rank
    (
        input_combined,
        input_combined_split_sizes,
        offsets_rearrange_list,
        offsets_rearrange_sizes,
        per_sample_weights,
        sharded_dim_size_max,
        padding_idx,
    ) = _sorted_input_distribute_prepare(
        input_split_sorted_list,
        input_split_sorted_indices,
        world_size,
        input,
        weight,
        per_sample_weights,
        rank,
        padding_idx,
    )

    # Send ID/offsets/per_sample_weights to different bucket(rank).
    (
        gathered_input,
        output_offsets_tensor_list,
        output_split_sizes,
        gathered_per_sample_weights,
    ) = _distribute_input(
        input_combined,
        input_combined_split_sizes,
        offsets_rearrange_list,
        offsets_rearrange_sizes,
        sharded_dim_size_max,
        world_size,
        input,
        per_sample_weights,
        pg,
    )

    # Perform the embedding bag look-up and aggregation
    results = []
    for i, inp in enumerate(gathered_input):
        per_sample_weights = (
            gathered_per_sample_weights[i]
            if gathered_per_sample_weights is not None
            else None
        )
        # If input is None, passing in max_norm causes
        # errors in CUDA.
        if max_norm is not None and inp.size(0) == 0:
            max_norm = None

        # Perform local embedding look up and aggregation.
        result = torch.nn.functional.embedding_bag(
            inp,
            local_shard,
            offsets=output_offsets_tensor_list[i],
            mode=mode if mode != "mean" else "sum",
            per_sample_weights=per_sample_weights,
            max_norm=max_norm,
            norm_type=norm_type,
            padding_idx=padding_idx,
        )
        if mode != "max":
            results.append(result)
        # For max case, it there is no look-up from some ranks
        # it will return all zero for that. For that case, we need
        # to set the row to neg inf; otherwise, in the final
        # aggregation negative values will be rounded up to zero.
        elif inp.size(0) == 0:
            result[:] = -float("Inf")
            results.append(result)
        else:
            for idx, current_offset in enumerate(output_offsets_tensor_list[i]):
                next_offset = current_offset
                if idx == len(output_offsets_tensor_list[i]) - 1:
                    next_offset = output_split_sizes[i]
                else:
                    next_offset = output_offsets_tensor_list[i][idx + 1]
                # When there is no interval in the current rank or all IDs
                # are equal to padding_idx, we then need to ensure they
                # don't contribute to the final result.
                if (current_offset == next_offset) or (
                    padding_idx is not None
                    and not torch.any(
                        torch.ne(inp[current_offset:next_offset], padding_idx)
                    )
                ):
                    result[idx] = -float("Inf")
            results.append(result)

    # Gather all the aggregated results appropriately by using reduce_scatter.
    row_size = input.size(0) if len(input_size) > 1 else len(split_sizes_1d)
    gathered_output = torch.empty(row_size, weight.size(1), device=input.device)
    op = ReduceOp.SUM if mode != "max" else ReduceOp.MAX
    dist.reduce_scatter(gathered_output, results, op=op, group=pg)

    # For Mean, we cannot do the division until very end because the sum of means
    # not equal to the mean of sum. (Divisor is different)
    if mode == "mean":
        split_sizes_1d_tensor = torch.tensor(
            split_sizes_1d_with_padding, dtype=torch.float, device=input.device
        )
        # Make sure divisor is not zero.
        split_sizes_1d_tensor[split_sizes_1d_tensor == 0.0] = 1.0
        return (
            torch.div(gathered_output.t().contiguous(), split_sizes_1d_tensor)
            .t()
            .contiguous()
        )

    # Return the appropriate local result.
    return gathered_output
