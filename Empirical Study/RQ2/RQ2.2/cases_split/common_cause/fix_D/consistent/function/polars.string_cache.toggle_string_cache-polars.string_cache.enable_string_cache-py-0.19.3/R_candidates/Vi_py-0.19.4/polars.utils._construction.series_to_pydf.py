def series_to_pydf(
    data: Series,
    schema: SchemaDefinition | None = None,
    schema_overrides: SchemaDict | None = None,
) -> PyDataFrame:
    """Construct a PyDataFrame from a Polars Series."""
    data_series = [data._s]
    series_name = [s.name() for s in data_series]
    column_names, schema_overrides = _unpack_schema(
        schema or series_name, schema_overrides=schema_overrides, n_expected=1
    )
    if schema_overrides:
        new_dtype = next(iter(schema_overrides.values()))
        if new_dtype != data.dtype:
            data_series[0] = data_series[0].cast(new_dtype, strict=True)

    data_series = _handle_columns_arg(data_series, columns=column_names)
    return PyDataFrame(data_series)
