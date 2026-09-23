@register_prop_rule(aten.index_select.default, schema_info=RuntimeSchemaInfo(1))
def prop_index_select(op_schema: OpSchema) -> OutputSharding:
    values_spec, dim, indices_spec = op_schema.args_schema

    assert isinstance(values_spec, DTensorSpec)
    assert isinstance(dim, int)
    assert isinstance(indices_spec, DTensorSpec)

    all_indices_spec: list[Optional[DTensorSpec]] = [
        indices_spec if dim == i else None for i in range(values_spec.ndim)
    ]

    result = prop_index(
        OpSchema(
            op=op_schema.op,
            args_schema=(values_spec, all_indices_spec),
            kwargs_schema=op_schema.kwargs_schema,
        )
    )
    if result.redistribute_schema:
        schema_suggestion = result.redistribute_schema
        result.redistribute_schema = OpSchema(
            op=op_schema.op,
            args_schema=(
                schema_suggestion.args_schema[0],
                dim,
                schema_suggestion.args_schema[1][dim],  # type: ignore[index]
            ),
            kwargs_schema=op_schema.kwargs_schema,
        )
    return result
