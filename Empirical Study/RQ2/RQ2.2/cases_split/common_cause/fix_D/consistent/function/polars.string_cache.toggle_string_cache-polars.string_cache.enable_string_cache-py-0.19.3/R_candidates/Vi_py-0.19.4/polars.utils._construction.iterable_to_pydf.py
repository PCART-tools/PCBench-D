def iterable_to_pydf(
    data: Iterable[Any],
    schema: SchemaDefinition | None = None,
    schema_overrides: SchemaDict | None = None,
    orient: Orientation | None = None,
    chunk_size: int | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
) -> PyDataFrame:
    """Construct a PyDataFrame from an iterable/generator."""
    original_schema = schema
    column_names: list[str] = []
    dtypes_by_idx: dict[int, PolarsDataType] = {}
    if schema is not None:
        column_names, schema_overrides = _unpack_schema(
            schema, schema_overrides=schema_overrides
        )
    elif schema_overrides:
        _, schema_overrides = _unpack_schema(schema, schema_overrides=schema_overrides)

    if not isinstance(data, Generator):
        data = iter(data)

    if orient == "col":
        if column_names and schema_overrides:
            dtypes_by_idx = {
                idx: schema_overrides.get(col, Unknown)
                for idx, col in enumerate(column_names)
            }

        return pl.DataFrame(
            {
                (column_names[idx] if column_names else f"column_{idx}"): pl.Series(
                    coldata, dtype=dtypes_by_idx.get(idx)
                )
                for idx, coldata in enumerate(data)
            }
        )._df

    def to_frame_chunk(values: list[Any], schema: SchemaDefinition | None) -> DataFrame:
        return pl.DataFrame(
            data=values,
            schema=schema,
            orient="row",
            infer_schema_length=infer_schema_length,
        )

    n_chunks = 0
    n_chunk_elems = 1_000_000

    if chunk_size:
        adaptive_chunk_size = chunk_size
    elif column_names:
        adaptive_chunk_size = n_chunk_elems // len(column_names)
    else:
        adaptive_chunk_size = None

    df: DataFrame = None  # type: ignore[assignment]
    chunk_size = max(
        (infer_schema_length or 0),
        (adaptive_chunk_size or 1000),
    )
    while True:
        values = list(islice(data, chunk_size))
        if not values:
            break
        frame_chunk = to_frame_chunk(values, original_schema)
        if df is None:
            df = frame_chunk
            if not original_schema:
                original_schema = list(df.schema.items())
            if chunk_size != adaptive_chunk_size:
                if (n_columns := len(df.columns)) > 0:
                    chunk_size = adaptive_chunk_size = n_chunk_elems // n_columns
        else:
            df.vstack(frame_chunk, in_place=True)
            n_chunks += 1

    if df is None:
        df = to_frame_chunk([], original_schema)

    return (df.rechunk() if n_chunks > 0 else df)._df
