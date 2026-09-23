def _handle_col_wise_sharding(
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
    pg,
):
    """
    Entry-point function to handle the logic of col-wise sharding of weight
    for embeddingBag. (Detailed explanations of the logic can be found in
    the comment for sharded_embedding_bag.)

    Args:
        input: list of ID used for lookup and aggregation.
        world_size: number of ranks.
        weight: shareded weight tensor.
        local_shard: col-wise shared local weight used for lookup.
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
        pg: process group.

    Return:
        output: final result of lookup and aggregation.
        local_shard: col-wise shared local weight used for lookup.
            If max_norm, this will be the renormed weight.
    """
    # allgather the special input of embedding bag first.
    gathered_per_sample_weights = None
    if per_sample_weights is not None:
        gathered_per_sample_weights = [
            torch.zeros_like(per_sample_weights) for _ in range(world_size)
        ]
        dist.all_gather(gathered_per_sample_weights, per_sample_weights, group=pg)
    gathered_offsets = None
    if offsets is not None:
        gathered_offsets = [torch.zeros_like(offsets) for _ in range(world_size)]
        dist.all_gather(gathered_offsets, offsets, group=pg)

    gathered_inputs = None
    if max_norm is not None:
        # max_norm changes the weight in-place
        local_shard, gathered_inputs = _handle_max_norm_col_wise(
            max_norm, norm_type, local_shard, input, world_size, pg
        )

    output = _handle_col_wise_sharding_base(
        torch.nn.functional.embedding_bag,
        1,
        input,
        world_size,
        weight,
        local_shard,
        pg,
        mode=mode,
        gathered_per_sample_weights=gathered_per_sample_weights,
        gathered_offsets=gathered_offsets,
        padding_idx=padding_idx,
        gathered_inputs=gathered_inputs,
    )
    return (output, local_shard)
