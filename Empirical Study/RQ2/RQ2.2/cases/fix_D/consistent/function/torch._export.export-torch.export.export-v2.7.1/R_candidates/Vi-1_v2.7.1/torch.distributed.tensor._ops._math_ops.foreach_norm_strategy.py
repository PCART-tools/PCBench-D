@register_op_strategy(
    [aten._foreach_norm.Scalar], schema_info=RuntimeSchemaInfo(1, needs_pytree=True)
)
def foreach_norm_strategy(op_schema: OpSchema) -> TupleStrategy:
    args_schema = op_schema.args_schema
    input_tuple_strategy = args_schema[0]
    assert isinstance(input_tuple_strategy, TupleStrategy)
    norm_type = args_schema[1] if len(args_schema) > 1 else 2
    assert isinstance(norm_type, (int, float, str)), f"{norm_type}"
    output_tuple_strategy_childs: list[OpStrategy] = []
    for op_strategy in input_tuple_strategy.childs:
        assert isinstance(op_strategy, OpStrategy), f"{op_strategy}"
        reduce_dims = list(range(op_strategy.ndim))
        output_strategy = common_reduction_strategy(
            op_strategy,
            reduce_dims,
            reduction_linear=True,
            reduction_op=NormReduction(norm_type),
        )
        output_tuple_strategy_childs.append(output_strategy)
    return TupleStrategy(output_tuple_strategy_childs)
