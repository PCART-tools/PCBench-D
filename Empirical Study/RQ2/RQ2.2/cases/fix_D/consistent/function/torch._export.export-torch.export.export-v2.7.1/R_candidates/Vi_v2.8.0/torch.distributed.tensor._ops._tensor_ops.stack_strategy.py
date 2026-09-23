@register_op_strategy(aten.stack.default, RuntimeSchemaInfo(1, needs_pytree=True))
def stack_strategy(op_schema: OpSchema) -> StrategyType:
    args_schema = op_schema.args_schema
    input_tuple_strategy = args_schema[0]
    assert isinstance(input_tuple_strategy, TupleStrategy), f"{input_tuple_strategy}"
    first_input_strategy = input_tuple_strategy.childs[0]
    assert isinstance(first_input_strategy, OpStrategy), f"{first_input_strategy}"
    common_input_ndim = first_input_strategy.ndim
    dim = cast(int, args_schema[1]) if len(args_schema) > 1 else 0
    # normalize the dim to be within the common input ndim
    dim = normalize_dim(dim, common_input_ndim)

    mesh = first_input_strategy.mesh

    follow_placements = _derive_follow_placements_from_tuple_strategy(
        op_schema.op, input_tuple_strategy
    )

    # create op strategy base on the follow placements
    op_strategy = OpStrategy([])

    input_specs = tuple(
        DTensorSpec(mesh, tuple(follow_placements))
        for _ in range(len(input_tuple_strategy.childs))
    )

    follow_placements = normalize_shard_for_stack(follow_placements, dim)

    op_strategy.strategies.append(
        OpSpec(
            output_specs=DTensorSpec(mesh, tuple(follow_placements)),
            input_specs=input_specs,
        )
    )
    return op_strategy
