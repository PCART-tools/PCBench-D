def _scan_parquet_fsspec(
    file: str,
    storage_options: dict[str, object] | None = None,
) -> LazyFrame:
    func = partial(_scan_parquet_impl, file, storage_options=storage_options)
    func_serialized = pickle.dumps(func)

    storage_options = storage_options or {}
    with _prepare_file_arg(file, **storage_options) as data:
        schema = polars.io.parquet.read_parquet_schema(data)

    return pli.LazyFrame._scan_python_function(schema, func_serialized)
