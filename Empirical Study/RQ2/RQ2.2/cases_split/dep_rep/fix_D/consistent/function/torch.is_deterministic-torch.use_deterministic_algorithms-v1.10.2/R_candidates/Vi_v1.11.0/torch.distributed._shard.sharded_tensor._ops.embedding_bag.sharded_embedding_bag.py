@sharded_op_impl(torch.nn.functional.embedding_bag)
def sharded_embedding_bag(types, args, kwargs, pg):
    """
    Handles ``__torch_function__`` dispatch for ``torch.nn.functional.embedding_bag``.
    This method computes a sharded embedding bag aggregation and has the following limitations:

    1. Supports only sharding of ``weight``.
    2. Supports only ``ChunkShardingSpec``.
    3. Supports only a single local shard per rank.
    4. Supports all specs except for scale_grad_by_freq, sparse, etc.

    Based on the dimension that the weight is sharded on, there are two
    algorithms:

    ROWWISE SHARDING
    ================
    For row-wise sharding the weight is sharded on dimension 0.

    The overall algorithm can be best explained with an example. Let's assume
    the dims for input are (4 x 6) and W are (16 x 17) and W is sharded across
    4 GPUs creating 4 shard of (4 x 17).
    The algorithm is as follows:

    1. First if the input is a 2D tensor, we sort by row. (If it's a 1D tensor, we sort
       the tensor per interval defined by offset.
       For example if the given input is generated within [1, 9] like
       tensor([[ 3,  7,  7,  9,  2,  1],
               [ 0,  0, 14,  5,  3, 12],
               [ 4,  5,  5,  9,  5, 13],
               [10,  3,  0,  7, 13,  9]])
       Then we have the sorted 2D tensor like:
       tensor([[ 1,  2,  3,  7,  7,  9],
               [ 0,  0,  3,  5, 12, 14],
               [ 4,  5,  5,  5,  9, 13],
               [ 0,  3,  7,  9, 10, 13]])
       Note if placement not equal to rank we will rearrange accordingly.
    2. Based on sorted result, we now have the offset like the following:
       [tensor([0, 3, 5, 6]), tensor([0, 3, 4, 4]),
        tensor([0, 0, 4, 5]), tensor([0, 2, 3, 5])]
       Note that embedding bag does allow the offset idx equal to length of
       input or repetitive. For these cases, it return a zero tensor.
    3. Next, we rearrange the sorted tensor into different ranks by first
       flattening it and grouping by ranks. Finally, we get a list of 1D tensors.
       So the given tensor now becomes:
       [tensor([1, 2, 3, 0, 0, 3, 0, 3]), tensor([7, 7, 5, 4, 5, 5, 5, 7]),
        tensor([9, 9, 9, 10]), tensor([12, 14, 13, 13])]
       We sync offsets with IDs. Offset now becomes:
       [tensor([0, 3, 6, 6]), tensor([0, 2, 3, 7]),
        tensor([0, 1, 1, 2]), tensor([0, 0, 2, 3])]
    5. Before we send out the array to other ranks, we need to do the modular operation
       so that each rank do use that for embedding look-up.
       The above ID tensor list will look like the below after performing the moduler of 4:
       [tensor([1, 2, 3, 0, 0, 3, 0, 3]), tensor([3, 3, 1, 0, 1, 1, 1, 3]),
        tensor([1, 1, 1, 2]), tensor([0, 2, 1, 1])]
    4. The example above only happens in one rank and each rank does a very similar thing
       with different rearranged IDs and offsets list. We then send IDs and offsets to the
       corresponding rank. Each rank do the look-up and aggregation on its local shard.
       We then use reduce_scatter to send the result back to each rank and perform the
       aggregation simultaneously.
    5. For "Mean" mode we need to divide by either column size (2D) or the interval length
       defined by the offset. We also need to mask the unexisting row to neg Inf so that
       negative value does not gets wiped out in the "Max" mode.

    COLWISE SHARDING
    ================
    For col-wise sharding the weight is sharded on dimension 1.

    The overall algorithm can be best explained with an example. Let's assume
    the dims for input are (4 x 6) and W are (16 x 17) and W is sharded across
    4 GPUs creating 3 shards of (16 x 5) and 1 shard of (16 x 2).
    The algorithm is as follows:

    1. First the input is broadcasted to all ranks, since this is SPMD we
       actually do an all_gather for all the inputs resulting in 4 (4 x 6)
       inputs on each rank.
    2. Next we perform local embedding bag operation under the given mode by
       apply each input (4 x 6) with the local shard (16 x 5) ((16 x 2) for the last).
       This results in 4 (5 x 4) ((2 x 4) for the last) matrices on each rank.
       We transpose the aggregation result.
    3. Next, we concatenate these 4 matrices and perform an all2all to share the
       appropriate (5 x 4) or (2 x 4) matrices to each rank.
    4. Now, each rank receives a (17 x 4) matrix which is basically the
       size of the result we need.
    5. If placements are not in order any appropriate rearrangement of columns
       are done for the (17 x 4) matrix and finally we transpose the output again.
    6. If max_norm is specified, we manually sum up the norm and renorm. Because
       the renorm must be in place, we need to override the local_shard to mimic
       this behavior.
    """
    # Validate input params
    _validate_embedding_bag_param(args, kwargs)

    input = args[0]
    weight = args[1]
    offsets = kwargs.get("offsets")
    per_sample_weights = kwargs.get("per_sample_weights")
    mode = kwargs.get("mode")
    max_norm = kwargs.get("max_norm")
    norm_type = kwargs.get("norm_type")
    include_last_offset = kwargs.get("include_last_offset")
    padding_idx = kwargs.get("padding_idx")

    local_shard = weight.local_tensor().contiguous()
    sharding_dim = weight._sharding_spec.dim
    world_size = dist.get_world_size(pg)
    rank = dist.get_rank(pg)
    if include_last_offset:
        offsets = offsets[:-1]

    if sharding_dim == 1:
        output, local_shard = _handle_col_wise_sharding(
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
        )
        weight.local_shards()[0].tensor = local_shard
        return output
    elif sharding_dim == 0:
        return _handle_row_wise_sharding(
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
        )
    else:
        raise RuntimeError(
            f"nn.EmbeddingBag weight sharded on dim {sharding_dim} not supported!"
        )
