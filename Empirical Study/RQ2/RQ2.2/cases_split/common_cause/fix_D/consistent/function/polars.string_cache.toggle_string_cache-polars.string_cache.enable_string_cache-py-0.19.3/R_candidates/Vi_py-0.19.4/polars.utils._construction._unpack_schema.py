def _unpack_schema(
    schema: SchemaDefinition | None,
    *,
    schema_overrides: SchemaDict | None = None,
    n_expected: int | None = None,
    lookup_names: Iterable[str] | None = None,
    include_overrides_in_columns: bool = False,
) -> tuple[list[str], SchemaDict]:
    """
    Unpack column names and create dtype lookup.

    Works for any (name, dtype) pairs or schema dict input,
    overriding any inferred dtypes with explicit dtypes if supplied.
    """
    # coerce schema_overrides to dict[str, PolarsDataType]
    if schema_overrides:
        schema_overrides = {
            name: dtype
            if is_polars_dtype(dtype, include_unknown=True)
            else py_type_to_dtype(dtype)
            for name, dtype in schema_overrides.items()
        }
    else:
        schema_overrides = {}

    # fastpath for empty schema
    if not schema:
        return (
            [f"column_{i}" for i in range(n_expected)] if n_expected else [],
            schema_overrides,
        )

    # determine column names from schema
    if isinstance(schema, dict):
        column_names: list[str] = list(schema)
        # coerce schema to list[str | tuple[str, PolarsDataType | PythonDataType | None]
        schema = list(schema.items())
    else:
        column_names = [
            (col or f"column_{i}") if isinstance(col, str) else col[0]
            for i, col in enumerate(schema)
        ]

    # determine column dtypes from schema and lookup_names
    lookup: dict[str, str] | None = (
        {col: name for col, name in zip_longest(column_names, lookup_names) if name}
        if lookup_names
        else None
    )
    column_dtypes: dict[str, PolarsDataType] = {
        lookup.get((name := col[0]), name)
        if lookup
        else col[0]: dtype  # type: ignore[misc]
        if is_polars_dtype(dtype, include_unknown=True)
        else py_type_to_dtype(dtype)
        for col in schema
        if isinstance(col, tuple) and (dtype := col[1]) is not None
    }

    # apply schema overrides
    if schema_overrides:
        column_dtypes.update(schema_overrides)

        if include_overrides_in_columns:
            column_names.extend(col for col in column_dtypes if col not in column_names)

    return column_names, column_dtypes
