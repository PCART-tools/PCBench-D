def _scan_ipc_fsspec(
    source: str,
    storage_options: dict[str, object] | None = None,
) -> LazyFrame:
    func = partial(_scan_ipc_impl, source, storage_options=storage_options)

    storage_options = storage_options or {}
    with _prepare_file_arg(source, **storage_options) as data:
        schema = polars.io.ipc.read_ipc_schema(data)

    return pl.LazyFrame._scan_python_function(schema, func)
