@register_op_strategy(
    [aten.linalg_vector_norm.default], schema_info=RuntimeSchemaInfo(1)
)
def vector_norm_strategy(op_schema: OpSchema) -> OpStrategy:
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    assert isinstance(input_strategy, OpStrategy)

    norm_type = args_schema[1] if len(args_schema) > 1 else 2
    assert isinstance(norm_type, (int, float, str)), f"{norm_type}"
    dim = args_schema[2] if len(args_schema) > 2 else None
    keepdim = args_schema[3] if len(args_schema) > 3 else False
    dims = _infer_reduction_dims(dim, input_strategy.ndim)
    reduce_dims = list(range(input_strategy.ndim)) if dims is None else dims
    return common_reduction_strategy(
        input_strategy,
        reduce_dims,
        keep_dim=cast(bool, keepdim),
        reduction_linear=True,
        reduction_op=NormReduction(norm_type),
    )
