def run_torchrec_row_wise_even_sharding_example(rank, world_size):
    # row-wise even sharding example:
    #   One table is evenly sharded by rows within the global ProcessGroup.
    #   In our example, the table's num_embedding is 8, and the embedding dim is 16
    #   The global ProcessGroup has 4 ranks, so each rank will have one 2 by 16 local
    #   shard.

    # device mesh is a representation of the worker ranks
    # create a 1-D device mesh that includes every rank
    device_type = get_device_type()
    device = torch.device(device_type)
    device_mesh = init_device_mesh(device_type=device_type, mesh_shape=(world_size,))

    # manually create the embedding table's local shards
    num_embeddings = 8
    embedding_dim = 16
    # tensor shape
    local_shard_shape = torch.Size(
        [num_embeddings // world_size, embedding_dim]  # (local_rows, local_cols)
    )
    # tensor offset
    local_shard_offset = torch.Size((rank * 2, embedding_dim))
    # tensor
    local_tensor = torch.randn(local_shard_shape, device=device)
    # row-wise sharding: one shard per rank
    # create the local shards wrapper
    local_shards_wrapper = LocalShardsWrapper(
        local_shards=[local_tensor],
        offsets=[local_shard_offset],
    )

    ###########################################################################
    # example 1: transform local_shards into DTensor
    # usage in TorchRec:
    #   ShardedEmbeddingCollection stores model parallel params in
    #   _model_parallel_name_to_sharded_tensor which is initialized in
    #   _initialize_torch_state() and torch.Tensor params are transformed
    #   into ShardedTensor by ShardedTensor._init_from_local_shards().
    #
    #   This allows state_dict() to always return ShardedTensor objects.

    # this is the sharding placement we use in DTensor to represent row-wise sharding
    # row_wise_sharding_placements means that the global tensor is sharded by first dim
    # over the 1-d mesh.
    row_wise_sharding_placements: list[Placement] = [Shard(0)]

    # create a DTensor from the local shard
    dtensor = DTensor.from_local(
        local_shards_wrapper, device_mesh, row_wise_sharding_placements, run_check=False
    )

    # display the DTensor's sharding
    visualize_sharding(dtensor, header="Row-wise even sharding example in DTensor")

    ###########################################################################
    # example 2: transform DTensor into local_shards
    # usage in TorchRec:
    #   In ShardedEmbeddingCollection's load_state_dict pre hook
    #   _pre_load_state_dict_hook, if the source param is a ShardedTensor
    #   then we need to transform it into its local_shards.

    # transform DTensor into LocalShardsWrapper
    dtensor_local_shards = dtensor.to_local()
    assert isinstance(dtensor_local_shards, LocalShardsWrapper)
    shard_tensor = dtensor_local_shards.shards[0]
    assert torch.equal(shard_tensor, local_tensor)
    assert dtensor_local_shards.shard_sizes[0] == local_shard_shape  # unwrap shape
    assert dtensor_local_shards.shard_offsets[0] == local_shard_offset  # unwrap offset
