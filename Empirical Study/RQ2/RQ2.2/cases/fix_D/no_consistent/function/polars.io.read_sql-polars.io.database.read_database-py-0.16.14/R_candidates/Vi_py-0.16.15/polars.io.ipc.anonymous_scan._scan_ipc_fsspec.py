def _scan_ipc_fsspec(
    file: str,
    storage_options: dict[str, object] | None = None,
) -> LazyFrame:
    func = partial(_scan_ipc_impl, file, storage_options=storage_options)
    func_serialized = pickle.dumps(func)

    storage_options = storage_options or {}
    with _prepare_file_arg(file, **storage_options) as data:
        schema = polars.io.ipc.read_ipc_schema(data)

    return pli.LazyFrame._scan_python_function(schema, func_serialized)
