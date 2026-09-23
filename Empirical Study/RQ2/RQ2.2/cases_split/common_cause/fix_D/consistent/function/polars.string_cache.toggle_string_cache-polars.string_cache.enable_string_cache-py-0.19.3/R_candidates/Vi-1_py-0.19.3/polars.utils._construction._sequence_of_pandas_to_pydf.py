def _sequence_of_pandas_to_pydf(
    first_element: pd.Series[Any] | pd.DatetimeIndex,
    data: Sequence[Any],
    schema: SchemaDefinition | None,
    schema_overrides: SchemaDict | None,
    **kwargs: Any,
) -> PyDataFrame:
    if schema is None:
        column_names: list[str] = []
    else:
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides, n_expected=1
        )

    schema_overrides = schema_overrides or {}
    data_series: list[PySeries] = []
    for i, s in enumerate(data):
        name = column_names[i] if column_names else s.name
        dtype = schema_overrides.get(name, None)
        pyseries = pandas_to_pyseries(name=name, values=s)
        if dtype is not None and dtype != pyseries.dtype():
            pyseries = pyseries.cast(dtype, strict=True)
        data_series.append(pyseries)

    return PyDataFrame(data_series)
