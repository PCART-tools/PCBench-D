@register_op_strategy(aten._scaled_dot_product_efficient_attention_backward.default)
def scaled_dot_product_efficient_attention_backward_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    # backward op does not need to validate the mesh since forward op has already done it
    mesh = op_schema.get_mesh_from_args(validate=False)

    q_input_strategy = op_schema.args_schema[1]
    assert isinstance(q_input_strategy, OpStrategy)
    # assuming q/k/v have the same shape
    has_attn_bias = op_schema.args_schema[4] is not None

    single_mesh_dim_strategies = []

    # placement list stores placements of [outputs, inputs]
    # in the spda backward case, we have 4 tensor outputs and 8 or 9 tensor inputs
    # NOTE: Output sharding of grad_bias on heads dim if attn_bias is present;
    #       otherwise grad_bias will be empty and its DTensorSpec will be removed.
    # first we can always accept full replication for both inputs and outputs
    all_replicate: PlacementList = [Replicate()] * (12 + has_attn_bias)

    if not has_attn_bias:
        all_replicate[3] = None  # grad bias is None if attn_bias is not present

    single_mesh_dim_strategies.append(all_replicate)

    # second we can accept the sharding pattern of tensor parallelism, which
    # shard on the heads dimension
    grad_output_sharding = Shard(1)
    qkv_sharding = Shard(1)
    output_sharding = Shard(1)
    logsumexp_sharding = Shard(1)
    grad_qkv_sharding = Shard(1)
    grad_bias_sharding = Shard(1) if has_attn_bias else None

    num_heads_dim_sharding: PlacementList = [
        grad_qkv_sharding,
        grad_qkv_sharding,
        grad_qkv_sharding,
        grad_bias_sharding,
        grad_output_sharding,
        qkv_sharding,
        qkv_sharding,
        qkv_sharding,
        # the place for optional input attn_bias,
        output_sharding,
        logsumexp_sharding,
    ]
    # input sharding of attn_bias on heads dim if present
    if has_attn_bias:
        num_heads_dim_sharding.insert(8, Shard(1))
    # accept replicate on the rest scalar tensor inputs
    # namely philox_seed and philox_offset
    num_heads_dim_sharding.extend([Replicate(), Replicate()])
    single_mesh_dim_strategies.append(num_heads_dim_sharding)

    # Context Parallelism: shards on the sequence dim
    seq_dim_sharding: PlacementList = [
        Shard(2),  # grad_q
        Shard(2),  # grad_k
        Shard(2),  # grad_v
        Shard(1) if has_attn_bias else None,  # grad_bias
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
    if has_attn_bias:
        num_heads_dim_sharding.insert(8, Shard(1))
    seq_dim_sharding.extend([Replicate(), Replicate()])
    single_mesh_dim_strategies.append(seq_dim_sharding)

    return expand_to_full_mesh_op_strategy(
        mesh,
        op_schema,
        single_mesh_dim_strategies,
        input_index=4,
    )
