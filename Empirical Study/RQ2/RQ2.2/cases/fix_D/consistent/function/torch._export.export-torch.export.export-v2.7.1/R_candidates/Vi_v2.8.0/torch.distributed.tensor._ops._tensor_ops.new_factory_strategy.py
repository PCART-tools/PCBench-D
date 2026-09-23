@register_op_strategy(
    [
        aten.new_empty.default,
        aten.new_full.default,
        aten.new_ones.default,
        aten.new_zeros.default,
        aten.new_empty_strided.default,
    ],
    schema_info=RuntimeSchemaInfo(1, ["dtype"]),
)
def new_factory_strategy(op_schema: OpSchema) -> StrategyType:
    # Currently there are two strategies:
    # 1. let the output be replicated
    # 2. let the output follow the input if input and output have the same shape
    input_strategy = op_schema.args_schema[0]
    assert isinstance(input_strategy, OpStrategy)

    mesh = input_strategy.mesh
    input_shape = input_strategy.shape
    output_shape = op_schema.args_schema[1]
    assert isinstance(output_shape, list)

    new_factory_strategy = OpStrategy([])
    for arg_strategy in input_strategy.strategies:
        input_spec = arg_strategy.output_spec
        replica_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
        new_factory_strategy.strategies.append(
            OpSpec(
                output_specs=replica_spec,
                input_specs=(input_spec,),
                redistribute_cost=[[0.0] * mesh.ndim],
            )
        )

        if tuple(input_shape) == tuple(output_shape) and input_spec.is_sharded():
            # NOTE: for new_empty_strided, currently the non-replicate sharding
            #       is supported only when the shape is evenly shardable
            if (
                op_schema.op == aten.new_empty_strided.default
                and not is_tensor_evenly_shardable(input_shape, input_spec)
            ):
                continue

            new_factory_strategy.strategies.append(
                OpSpec(
                    output_specs=input_spec,
                    input_specs=(input_spec,),
                    # encouraging new tensor placement to be the same as input
                    redistribute_cost=[[-0.1] * mesh.ndim],
                )
            )

    return new_factory_strategy
