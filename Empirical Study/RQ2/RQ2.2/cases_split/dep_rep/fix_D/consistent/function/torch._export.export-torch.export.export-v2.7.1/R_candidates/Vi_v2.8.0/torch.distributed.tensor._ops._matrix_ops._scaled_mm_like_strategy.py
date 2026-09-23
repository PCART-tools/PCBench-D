def _scaled_mm_like_strategy(
    mm_equation: str, mesh: DeviceMesh, op_schema: OpSchema
) -> OpStrategy:
    (
        self_strategy,
        mat2_strategy,
        scale_self_strategy,
        scale_mat2_strategy,
        bias_strategy,
        scale_result_strategy,
        *_,
    ) = op_schema.args_schema
    assert isinstance(self_strategy, OpStrategy)
    assert isinstance(mat2_strategy, OpStrategy)
    assert isinstance(scale_self_strategy, OpStrategy)
    assert isinstance(scale_mat2_strategy, OpStrategy)
    # TODO: add support for these later
    assert bias_strategy is None, "_scaled_mm on DTensors doesn't support bias"
    assert scale_result_strategy is None, (
        "_scaled_mm on DTensors doesn't support scale_result"
    )
    # generate all possible strategies for mm
    mm_strategy = gen_einsum_strategies(mm_equation, mesh)
    # filter out invalid strategies and associate costs
    strategies = mm_strategy.strategies
    filtered_strategies = []
    for strtg in strategies:
        assert strtg.input_specs is not None
        self_spec = strtg.input_specs[0]
        mat2_spec = strtg.input_specs[1]
        # propagate the operands' specs to their scales, except for tensor-wise
        # scaling which can have any numbers of dims (legacy...), hence sharding
        # dims won't map. for tensor-wise, anyways, we can only do replication.
        scale_self_spec = (
            DTensorSpec(self_spec.mesh, (Replicate(),))
            if prod(scale_self_strategy.shape) == 1
            else self_spec
        )
        scale_mat2_spec = (
            DTensorSpec(mat2_spec.mesh, (Replicate(),))
            if prod(scale_mat2_strategy.shape) == 1
            else mat2_spec
        )
        strtg.input_specs = list(strtg.input_specs) + [scale_self_spec, scale_mat2_spec]
        if (
            is_tensor_shardable(self_strategy.shape, self_spec)
            and is_tensor_shardable(mat2_strategy.shape, mat2_spec)
            and is_tensor_shardable(scale_self_strategy.shape, scale_self_spec)
            and is_tensor_shardable(scale_mat2_strategy.shape, scale_mat2_spec)
        ):
            redistribute_cost = [
                generate_redistribute_costs(self_strategy, self_spec),
                generate_redistribute_costs(mat2_strategy, mat2_spec),
                generate_redistribute_costs(scale_self_strategy, scale_self_spec),
                generate_redistribute_costs(scale_mat2_strategy, scale_mat2_spec),
            ]
            strtg.redistribute_cost = redistribute_cost
            filtered_strategies.append(strtg)

    mm_strategy.strategies = filtered_strategies

    return mm_strategy
