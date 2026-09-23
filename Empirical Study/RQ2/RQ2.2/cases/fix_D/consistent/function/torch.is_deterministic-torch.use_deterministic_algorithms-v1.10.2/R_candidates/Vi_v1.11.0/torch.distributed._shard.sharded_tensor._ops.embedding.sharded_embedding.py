@sharded_op_impl(torch.nn.functional.embedding)
def sharded_embedding(types, args, kwargs, pg):
    """
    Handles ``__torch_function__`` dispatch for ``torch.nn.functional.embedding``.
    This method computes a sharded embedding lookup and has the following limitations:

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
    the dims for input are (4 x 6) and W are (10 x 17) and W is sharded across
    4 GPUs creating 3 shard of (3 x 17) and 1 shard of (1 x 17).
    The algorithm is as follows:

    1. First the input is flattened to 1D and gets sorted so that we can distribute
       them to the corresponding rank. For example if the given input is
       tensor([[6, 5, 2, 9, 6, 3],
               [3, 1, 2, 4, 7, 6],
               [4, 0, 4, 9, 8, 9],
               [8, 6, 6, 4, 6, 1]])
       Then we have the 1D array like:
       tensor([6, 5, 2, 9, 6, 3, 3, 1, 2, 4, 7, 6, 4, 0, 4, 9, 8, 9, 8, 6, 6, 4, 6, 1])
       And sort it:
       tensor([0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 6, 6, 6, 6, 6, 6, 7, 8, 8, 9, 9, 9])
       We also record the indices so that we can recover back.
    2. Next we perform the split by search the index of the chunking
       boundary. So the above array will be split into 4 parts:
       tensor([[0, 1, 1, 2, 2], [3, 3, 4, 4, 4, 4, 5],
              [6, 6, 6, 6, 6, 6, 7, 8, 8], [9, 9, 9])
       Rearrangement may be needed if the rank order is different from
       its index in the placement.
    3. Next, we communicate the length of each part to each rank via all2all
       so that each rank now knows what input it will get from all other ranks.
    4. Before we send out the array to other ranks, we need to do the modular operation
       so that each rank do use that for embedding lookup.
       The above tensor will look like the below after performing the moduler of 3:
       tensor([[0, 1, 1, 2, 2], [0, 0, 1, 1, 1, 1, 2],
              [0, 0, 0, 0, 0, 0, 1, 2, 2], [0, 0, 0])
    5. Now, each rank receives a matrix (size may vary) and do the lookup. We then use
       all2all to send the result back to each rank.
    6. We use the recorded indices to recover the sorted positions and reshape the
       matrix to (4 x 6 x 17), which is what we need.

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
    2. Next we perform local embedding lookup operation by apply each
       input (4 x 6) with the local shard (16 x 5) ((16 x 2) for the last).
       This results in 4 (5 x 6 x 4) ((2 x 6 x 4) for the last) matrices
       on each rank. We transpose dim 0 and dim 2.
    3. Next, we concat these 4 matrices and perform an all2all to share the
       appropriate (5 x 6 x 4) or (2 x 6 x 4) matrices to each rank.
    4. Now, each rank receives a (17 x 6 x 4) matrix which is basically the
       size of the result we need.
    5. If placements are not in order any appropriate rearrangement of columns
       are done for the (17 x 6 x 4) matrix and finally we transpose the
       dim 0 and dim 2 again.
    6. If max_norm is specified, we manually sum up the norm and renorm. Because
       the renorm must be in place, we need to override the local_shard to mimic
       this behavior.
    """
    # Validate input params
    _validate_embedding_param(args, kwargs)

    input = args[0]
    weight = args[1]
    max_norm = kwargs.get("max_norm")
    norm_type = kwargs.get("norm_type")
    padding_idx = kwargs.get("padding_idx")

    local_shard = weight.local_tensor().contiguous()
    sharding_dim = weight._sharding_spec.dim
    world_size = dist.get_world_size(pg)
    rank = dist.get_rank(pg)

    if sharding_dim == 1:
        output, local_shard = _handle_col_wise_sharding(
            input, world_size, weight, local_shard, max_norm, norm_type, padding_idx, pg
        )
        weight.local_shards()[0].tensor = local_shard
        return output
    elif sharding_dim == 0:
        return _handle_row_wise_sharding(
            input,
            world_size,
            weight,
            local_shard,
            max_norm,
            norm_type,
            padding_idx,
            rank,
            pg,
        )
    else:
        raise RuntimeError(
            f"nn.Embedding weight sharded on dim {sharding_dim} not supported!"
        )
