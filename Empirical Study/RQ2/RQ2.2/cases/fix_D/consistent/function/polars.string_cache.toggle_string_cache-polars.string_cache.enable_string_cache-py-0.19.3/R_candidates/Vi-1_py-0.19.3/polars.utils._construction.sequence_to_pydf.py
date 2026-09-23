def sequence_to_pydf(
    data: Sequence[Any],
    schema: SchemaDefinition | None = None,
    schema_overrides: SchemaDict | None = None,
    orient: Orientation | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
) -> PyDataFrame:
    """Construct a PyDataFrame from a sequence."""
    if len(data) == 0:
        return dict_to_pydf({}, schema=schema, schema_overrides=schema_overrides)

    return _sequence_to_pydf_dispatcher(
        data[0],
        data=data,
        schema=schema,
        schema_overrides=schema_overrides,
        orient=orient,
        infer_schema_length=infer_schema_length,
    )
