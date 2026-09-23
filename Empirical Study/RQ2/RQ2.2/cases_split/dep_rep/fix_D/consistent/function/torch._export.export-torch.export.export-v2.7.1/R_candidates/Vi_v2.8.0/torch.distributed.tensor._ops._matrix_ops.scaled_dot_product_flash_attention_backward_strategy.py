@register_op_strategy(aten._scaled_dot_product_flash_attention_backward.default)
def scaled_dot_product_flash_attention_backward_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    # backward op does not need to validate the mesh since forward op has already done it
    mesh = op_schema.get_mesh_from_args(validate=False)

    q_input_strategy = op_schema.args_schema[1]
    assert isinstance(q_input_strategy, OpStrategy)
    # assuming q/k/v have the same shape

    tensor_input_indices = [
        i
        for i, arg_spec in enumerate(op_schema.args_schema)
        if isinstance(arg_spec, OpStrategy)
    ]
    num_tensor_inputs = len(tensor_input_indices)

    single_mesh_dim_strategies = []

    # placement list stores placements of [outputs, inputs]
    # in the spda backward case, we have 3 tensor outputs and 6 to 10 tensor inputs
    # first we can always accept full replication for both inputs and outputs
    all_replicate: PlacementList = [Replicate()] * (3 + num_tensor_inputs)

    single_mesh_dim_strategies.append(all_replicate)

    # second we can accept the sharding pattern of tensor parallelism, which
    # shard on the num of head dim
    grad_output_sharding = Shard(1)  # num head dim
    qkv_sharding = Shard(1)  # num head dim
    output_sharding = Shard(1)  # num head dim
    logsumexp_sharding = Shard(1)  # num head dim
    grad_qkv_sharding = Shard(1)  # num head dim

    num_heads_dim_sharding: PlacementList = [
        grad_qkv_sharding,
        grad_qkv_sharding,
        grad_qkv_sharding,
        grad_output_sharding,
        qkv_sharding,
        qkv_sharding,
        qkv_sharding,
        output_sharding,
        logsumexp_sharding,
    ]
    # accept replicate on the rest tensor inputs, potentially
    # cum_seq_q, cum_seq_k, philox_seed, philox_offset
    # at indices 6, 7, 12, 13, respectively
    num_heads_dim_sharding.extend([Replicate()] * (num_tensor_inputs - 6))
    single_mesh_dim_strategies.append(num_heads_dim_sharding)

    # Batch sharding
    batch_dim_sharding: PlacementList = [
        Shard(0),  # grad_q
        Shard(0),  # grad_k
        Shard(0),  # grad_v
        Shard(0),  # grad_output
        Shard(0),  # q
        Shard(0),  # k
        Shard(0),  # v
        Shard(0),  # output
        Shard(0),  # logsumexp
    ]
    # accept replicate on the rest tensor inputs, potentially
    # cum_seq_q, cum_seq_k, philox_seed, philox_offset
    # at indices 6, 7, 12, 13, respectively
    batch_dim_sharding.extend([Replicate()] * (num_tensor_inputs - 6))
    single_mesh_dim_strategies.append(batch_dim_sharding)

    # Context Parallelism: shards on the sequence dim
    seq_dim_sharding: PlacementList = [
        Shard(2),  # grad_q
        Shard(2),  # grad_k
        Shard(2),  # grad_v
        Shard(2),  # grad_output
        Shard(2),  # q
        Shard(2),  # k
        Shard(2),  # v
        Shard(2),  # output
        Shard(2),  # logsumexp
    ]
    # accept replicate on the rest tensor inputs, potentially
    # cum_seq_q, cum_seq_k, philox_seed, philox_offset
    # at indices 6, 7, 12, 13, respectively
    seq_dim_sharding.extend([Replicate()] * (num_tensor_inputs - 6))
    single_mesh_dim_strategies.append(seq_dim_sharding)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=3
    )
