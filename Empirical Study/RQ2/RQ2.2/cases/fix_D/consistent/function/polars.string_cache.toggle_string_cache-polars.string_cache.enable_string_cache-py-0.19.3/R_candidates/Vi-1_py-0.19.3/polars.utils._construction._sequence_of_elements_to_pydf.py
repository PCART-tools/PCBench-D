@_sequence_to_pydf_dispatcher.register(str)
def _sequence_of_elements_to_pydf(
    first_element: Any,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    **kwargs: Any,
) -> PyDataFrame:
    column_names, schema_overrides = _unpack_schema(
        schema, schema_overrides=schema_overrides, n_expected=1
    )
    data_series: list[PySeries] = [
        pl.Series(column_names[0], data, schema_overrides.get(column_names[0]))._s
    ]
    data_series = _handle_columns_arg(data_series, columns=column_names)
    return PyDataFrame(data_series)
