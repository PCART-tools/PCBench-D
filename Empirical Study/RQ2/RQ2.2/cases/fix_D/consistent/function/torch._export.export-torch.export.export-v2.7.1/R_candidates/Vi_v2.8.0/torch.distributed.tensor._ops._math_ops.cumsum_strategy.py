@register_op_strategy(aten.cumsum.default, schema_info=RuntimeSchemaInfo(1))
def cumsum_strategy(op_schema: OpSchema) -> OpStrategy:
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    assert isinstance(input_strategy, OpStrategy)
    dim = args_schema[1]
    assert isinstance(dim, int), f"{dim}"

    return common_reduction_strategy(
        input_strategy, [dim], keep_dim=True, reduction_linear=False
    )
