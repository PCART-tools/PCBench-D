def pandas_to_pydf(
    data: pd.DataFrame,
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    rechunk: bool = True,
    nan_to_null: bool = True,
    include_index: bool = False,
) -> PyDataFrame:
    """Construct a PyDataFrame from a pandas DataFrame."""
    arrow_dict = {}
    length = data.shape[0]

    if include_index and not pandas_has_default_index(data):
        for idxcol in data.index.names:
            arrow_dict[str(idxcol)] = _pandas_series_to_arrow(
                data.index.get_level_values(idxcol),
                nan_to_null=nan_to_null,
                length=length,
            )

    for col in data.columns:
        arrow_dict[str(col)] = _pandas_series_to_arrow(
            data[col], nan_to_null=nan_to_null, length=length
        )

    arrow_table = pa.table(arrow_dict)
    return arrow_to_pydf(
        arrow_table, schema=schema, schema_overrides=schema_overrides, rechunk=rechunk
    )
