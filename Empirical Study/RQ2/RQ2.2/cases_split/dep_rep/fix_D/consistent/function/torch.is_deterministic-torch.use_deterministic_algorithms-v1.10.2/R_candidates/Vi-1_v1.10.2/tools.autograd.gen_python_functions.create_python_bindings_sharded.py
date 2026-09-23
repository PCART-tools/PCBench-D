def create_python_bindings_sharded(
    fm: FileManager,
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    pred: Callable[[NativeFunction], bool],
    module: Optional[str],
    filename: str,
    *,
    method: bool,
    num_shards: int
) -> None:
    """Generates Python bindings to ATen functions"""
    grouped = group_filter_overloads(pairs, pred)

    def key_func(kv: Tuple[BaseOperatorName, List[PythonSignatureNativeFunctionPair]]) -> str:
        return str(kv[0])

    def env_func(
        kv: Tuple[BaseOperatorName, List[PythonSignatureNativeFunctionPair]]
    ) -> Dict[str, List[str]]:
        return {
            'py_forwards': list(forward_decls(kv[0], kv[1], method=method)),
            'py_methods': [method_impl(kv[0], module, kv[1], method=method)],
            'py_method_defs': [method_def(kv[0], module, kv[1], method=method)],
        }

    fm.write_sharded(
        filename,
        grouped.items(),
        base_env={
            'generated_comment':
            '@' + f'generated from {fm.template_dir}/{filename}',
        },
        key_fn=key_func,
        env_callable=env_func,
        num_shards=num_shards,
        sharded_keys={'py_forwards', 'py_methods', 'py_method_defs'}
    )
