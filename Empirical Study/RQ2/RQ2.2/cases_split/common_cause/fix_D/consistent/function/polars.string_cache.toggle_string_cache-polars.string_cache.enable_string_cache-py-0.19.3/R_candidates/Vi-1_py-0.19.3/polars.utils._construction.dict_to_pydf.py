def dict_to_pydf(
    data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    nan_to_null: bool = False,
) -> PyDataFrame:
    """Construct a PyDataFrame from a dictionary of sequences."""
    if isinstance(schema, dict) and data:
        if not all((col in schema) for col in data):
            raise ValueError(
                "the given column-schema names do not match the data dictionary"
            )
        data = {col: data[col] for col in schema}

    column_names, schema_overrides = _unpack_schema(
        schema, lookup_names=data.keys(), schema_overrides=schema_overrides
    )
    if not column_names:
        column_names = list(data)

    if data and _NUMPY_AVAILABLE:
        # if there are 3 or more numpy arrays of sufficient size, we multi-thread:
        count_numpy = sum(
            int(
                _check_for_numpy(val)
                and isinstance(val, np.ndarray)
                and len(val) > 1000
            )
            for val in data.values()
        )
        if count_numpy >= 3:
            # yes, multi-threading was easier in python here; we cannot have multiple
            # threads running python and release the gil in pyo3 (it will deadlock).

            # (note: 'dummy' is threaded)
            import multiprocessing.dummy

            pool_size = threadpool_size()
            with multiprocessing.dummy.Pool(pool_size) as pool:
                data = dict(
                    zip(
                        column_names,
                        pool.map(
                            lambda t: pl.Series(t[0], t[1])
                            if isinstance(t[1], np.ndarray)
                            else t[1],
                            [(k, v) for k, v in data.items()],
                        ),
                    )
                )

    if not data and schema_overrides:
        data_series = [
            pl.Series(
                name, [], dtype=schema_overrides.get(name), nan_to_null=nan_to_null
            )._s
            for name in column_names
        ]
    else:
        data_series = [
            s._s
            for s in _expand_dict_scalars(
                data, schema_overrides=schema_overrides, nan_to_null=nan_to_null
            ).values()
        ]

    data_series = _handle_columns_arg(data_series, columns=column_names, from_dict=True)
    pydf = PyDataFrame(data_series)

    if schema_overrides and pydf.dtypes() != list(schema_overrides.values()):
        pydf = _post_apply_columns(
            pydf, column_names, schema_overrides=schema_overrides
        )
    return pydf
