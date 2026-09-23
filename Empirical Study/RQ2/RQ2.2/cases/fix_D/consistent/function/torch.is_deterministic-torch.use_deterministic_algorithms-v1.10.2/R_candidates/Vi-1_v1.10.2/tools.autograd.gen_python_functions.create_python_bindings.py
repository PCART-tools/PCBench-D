def create_python_bindings(
    fm: FileManager,
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    pred: Callable[[NativeFunction], bool],
    module: Optional[str],
    filename: str,
    *,
    method: bool,
) -> None:
    """Generates Python bindings to ATen functions"""
    py_methods: List[str] = []
    py_method_defs: List[str] = []
    py_forwards: List[str] = []

    grouped = group_filter_overloads(pairs, pred)

    for name in sorted(grouped.keys(), key=lambda x: str(x)):
        overloads = grouped[name]
        py_methods.append(method_impl(name, module, overloads, method=method))
        py_method_defs.append(method_def(name, module, overloads, method=method))
        py_forwards.extend(forward_decls(name, overloads, method=method))

    fm.write_with_template(filename, filename, lambda: {
        'generated_comment': '@' + f'generated from {fm.template_dir}/{filename}',
        'py_forwards': py_forwards,
        'py_methods': py_methods,
        'py_method_defs': py_method_defs,
    })
