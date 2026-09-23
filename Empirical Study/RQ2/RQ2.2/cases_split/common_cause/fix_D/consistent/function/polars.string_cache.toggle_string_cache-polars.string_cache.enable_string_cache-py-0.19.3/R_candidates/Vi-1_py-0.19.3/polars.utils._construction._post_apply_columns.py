def _post_apply_columns(
    pydf: PyDataFrame,
    columns: SchemaDefinition | None,
    structs: dict[str, Struct] | None = None,
    schema_overrides: SchemaDict | None = None,
) -> PyDataFrame:
    """Apply 'columns' param _after_ PyDataFrame creation (if no alternative)."""
    pydf_columns, pydf_dtypes = pydf.columns(), pydf.dtypes()
    columns, dtypes = _unpack_schema(
        (columns or pydf_columns), schema_overrides=schema_overrides
    )
    column_subset: list[str] = []
    if columns != pydf_columns:
        if len(columns) < len(pydf_columns) and columns == pydf_columns[: len(columns)]:
            column_subset = columns
        else:
            pydf.set_column_names(columns)

    column_casts = []
    for i, col in enumerate(columns):
        dtype = dtypes.get(col)
        pydf_dtype = pydf_dtypes[i]
        if dtype == Categorical != pydf_dtype:
            column_casts.append(F.col(col).cast(Categorical)._pyexpr)
        elif structs and (struct := structs.get(col)) and struct != pydf_dtype:
            column_casts.append(F.col(col).cast(struct)._pyexpr)
        elif dtype is not None and dtype != Unknown and dtype != pydf_dtype:
            column_casts.append(F.col(col).cast(dtype)._pyexpr)

    if column_casts or column_subset:
        pydf = pydf.lazy()
        if column_casts:
            pydf = pydf.with_columns(column_casts)
        if column_subset:
            pydf = pydf.select([F.col(col)._pyexpr for col in column_subset])
        pydf = pydf.collect()

    return pydf
