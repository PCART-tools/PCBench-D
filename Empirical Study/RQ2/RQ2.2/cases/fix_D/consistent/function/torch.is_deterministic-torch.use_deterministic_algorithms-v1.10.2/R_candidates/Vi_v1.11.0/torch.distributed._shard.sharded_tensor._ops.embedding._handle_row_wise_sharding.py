def _handle_row_wise_sharding(
    input, world_size, weight, local_shard, max_norm, norm_type, padding_idx, rank, pg
):
    """
    Entry-point function to handle the logic of row-wise sharding of weight
    for embedding. (Detailed explanations of the logic can be found in
    the comment for sharded_embedding.)

    Args:
        input: list of ID used for lookup and aggregation.
        world_size: number of ranks.
        weight: shareded weight tensor.
        local_shard: row-wise shared local weight used for lookup.
        max_norm: If given, each embedding vector with norm larger
            than max_norm is renormalized to have norm max_norm.
            Note: this will modify weight in-place.
        norm_type: The p in the p-norm to compute for the max_norm option.
        padding_idx: If specified, the entries at padding_idx do
            not contribute to the gradient; therefore, the embedding
            vector at padding_idx is not updated during training,
            i.e. it remains as a fixed “pad”.
        rank: # of cuda process.
        pg: process group.

    Returns: final result of lookup.
    """
    # flatten the ids across all input and sort
    input_size = input.size()
    input_1d = torch.reshape(input, (-1,)).contiguous()
    input_sorted, indices_1d = torch.sort(input_1d)
    rearrange_indices_1d = torch.argsort(indices_1d)
    input_sorted.contiguous()

    (
        input_sorted,
        input_split_sizes,
        sharded_dim_size_max,
        _,
        rearrange_indices_1d_second_order,
        padding_idx,
    ) = _handle_row_wise_lookup_distribute(
        input_sorted, input, world_size, weight, rank, padding_idx
    )

    # Get the input split size to be sent from each rank to the current rank.
    # We can then infer the output split size.
    output_split_sizes = _communicate_size_to_each_rank(
        input_split_sizes, world_size, input, pg
    )

    # Input sent from each rank to the current rank may have different sizes.
    gathered_input = torch.empty(
        sum(output_split_sizes), dtype=torch.int64, device=input.device
    )

    # Perform the modular operation of the 1D tensor to be sent to each rank.
    input_sorted = torch.remainder(input_sorted, sharded_dim_size_max)

    # Perform alltoall
    dist.all_to_all_single(
        gathered_input,
        input_sorted,
        input_split_sizes=input_split_sizes,
        output_split_sizes=output_split_sizes,
        group=pg,
    )

    # If input is None, passing in max_norm causes
    # errors in CUDA.
    if max_norm is not None and gathered_input.size(0) == 0:
        max_norm = None

    # Perform local embedding look up.
    gathered_input_embeddings = torch.nn.functional.embedding(
        gathered_input,
        local_shard,
        padding_idx=padding_idx,
        max_norm=max_norm,
        norm_type=norm_type,
    )

    # Gather all lookup result appropriately by performing alltoall again
    gathered_output = torch.empty(
        input_sorted.size(0), weight.size(1), device=input.device
    )
    dist.all_to_all_single(
        gathered_output,
        gathered_input_embeddings,
        input_split_sizes=output_split_sizes,
        output_split_sizes=input_split_sizes,
        group=pg,
    )

    # Rearrange the results to its original shape.
    if rearrange_indices_1d_second_order is not None:
        gathered_output = gathered_output[rearrange_indices_1d_second_order]
    gathered_output = gathered_output[rearrange_indices_1d]

    # Return the appropriate local result.
    return torch.reshape(gathered_output, (*input_size, weight.size(1)))
