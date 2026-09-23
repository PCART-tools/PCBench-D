def _sequence_of_series_to_pydf(
    first_element: Series,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    **kwargs: Any,
) -> PyDataFrame:
    series_names = [s.name for s in data]
    column_names, schema_overrides = _unpack_schema(
        schema or series_names,
        schema_overrides=schema_overrides,
        n_expected=len(data),
    )
    data_series: list[PySeries] = []
    for i, s in enumerate(data):
        if not s.name:
            s = s.alias(column_names[i])
        new_dtype = schema_overrides.get(column_names[i])
        if new_dtype and new_dtype != s.dtype:
            s = s.cast(new_dtype)
        data_series.append(s._s)

    data_series = _handle_columns_arg(data_series, columns=column_names)
    return PyDataFrame(data_series)
