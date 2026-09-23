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
        return kv[0].base

    def env_func(
        kv: Tuple[BaseOperatorName, List[PythonSignatureNativeFunctionPair]]
    ) -> Dict[str, List[str]]:
        name, fn_pairs = kv
        return {
            'ops_headers': [f'#include <ATen/ops/{name.base}.h>'],
            'py_forwards': list(forward_decls(name, fn_pairs, method=method)),
            'py_methods': [method_impl(name, module, fn_pairs, method=method)],
            'py_method_defs': [method_def(name, module, fn_pairs, method=method)],
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
        sharded_keys={'ops_headers', 'py_forwards', 'py_methods', 'py_method_defs'}
    )
