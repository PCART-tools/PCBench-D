def arrow_to_pydf(
    data: pa.Table,
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    rechunk: bool = True,
) -> PyDataFrame:
    """Construct a PyDataFrame from an Arrow Table."""
    original_schema = schema
    column_names, schema_overrides = _unpack_schema(
        (schema or data.column_names), schema_overrides=schema_overrides
    )
    try:
        if column_names != data.column_names:
            data = data.rename_columns(column_names)
    except pa.lib.ArrowInvalid as e:
        raise ValueError("dimensions of columns arg must match data dimensions") from e

    data_dict = {}
    # dictionaries cannot be built in different batches (categorical does not allow
    # that) so we rechunk them and create them separately.
    dictionary_cols = {}
    # struct columns don't work properly if they contain multiple chunks.
    struct_cols = {}
    names = []
    for i, column in enumerate(data):
        # extract the name before casting
        name = f"column_{i}" if column._name is None else column._name
        names.append(name)

        column = coerce_arrow(column)
        if pa.types.is_dictionary(column.type):
            ps = arrow_to_pyseries(name, column, rechunk=rechunk)
            dictionary_cols[i] = wrap_s(ps)
        elif isinstance(column.type, pa.StructType) and column.num_chunks > 1:
            ps = arrow_to_pyseries(name, column, rechunk=rechunk)
            struct_cols[i] = wrap_s(ps)
        else:
            data_dict[name] = column

    if len(data_dict) > 0:
        tbl = pa.table(data_dict)

        # path for table without rows that keeps datatype
        if tbl.shape[0] == 0:
            pydf = pl.DataFrame(
                [pl.Series(name, c) for (name, c) in zip(tbl.column_names, tbl.columns)]
            )._df
        else:
            pydf = PyDataFrame.from_arrow_record_batches(tbl.to_batches())
    else:
        pydf = pl.DataFrame([])._df
    if rechunk:
        pydf = pydf.rechunk()

    reset_order = False
    if len(dictionary_cols) > 0:
        df = wrap_df(pydf)
        df = df.with_columns([F.lit(s).alias(s.name) for s in dictionary_cols.values()])
        reset_order = True

    if len(struct_cols) > 0:
        df = wrap_df(pydf)
        df = df.with_columns([F.lit(s).alias(s.name) for s in struct_cols.values()])
        reset_order = True

    if reset_order:
        df = df[names]
        pydf = df._df

    if column_names != original_schema and (schema_overrides or original_schema):
        pydf = _post_apply_columns(
            pydf, original_schema, schema_overrides=schema_overrides
        )
    elif schema_overrides:
        for col, dtype in zip(pydf.columns(), pydf.dtypes()):
            override_dtype = schema_overrides.get(col)
            if override_dtype is not None and dtype != override_dtype:
                pydf = _post_apply_columns(
                    pydf, original_schema, schema_overrides=schema_overrides
                )
                break

    return pydf
