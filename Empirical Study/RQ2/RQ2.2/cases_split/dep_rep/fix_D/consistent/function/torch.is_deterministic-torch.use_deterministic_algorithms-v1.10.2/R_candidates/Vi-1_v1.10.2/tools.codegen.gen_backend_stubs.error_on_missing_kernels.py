def error_on_missing_kernels(
        native_functions: Sequence[NativeFunction],
        backend_indices: Dict[DispatchKey, BackendIndex],
        backend_key: DispatchKey,
        autograd_key: DispatchKey,
        kernel_defn_file_path: str,
) -> None:
    try:
        with open(kernel_defn_file_path, 'r') as f:
            backend_defns = f.read()
    except IOError:
        raise AssertionError(f'Unable to read from the specified impl_path file: {kernel_defn_file_path}')

    class_name: Optional[str] = backend_indices[backend_key].native_function_class_name()
    assert class_name is not None

    expected_backend_op_names: List[OperatorName] = \
        list(backend_indices[backend_key].index.keys()) + list(backend_indices[autograd_key].index.keys())
    expected_backend_native_funcs: List[NativeFunction] = [f for f in native_functions if f.func.name in expected_backend_op_names]
    expected_backend_kernel_name_counts: Dict[str, List[NativeFunction]] = defaultdict(list)
    for native_f in expected_backend_native_funcs:
        expected_backend_kernel_name_counts[dispatcher.name(native_f.func)].append(native_f)

    kernel_defn_regex = rf'{class_name}::([\w\d]*)\([^\)]*\)\s*{{'
    actual_backend_kernel_name_counts = Counter(re.findall(kernel_defn_regex, backend_defns))

    missing_kernels_err_msg = ""
    for expected_name, funcs in expected_backend_kernel_name_counts.items():
        expected_overload_count = len(funcs)
        actual_overload_count = actual_backend_kernel_name_counts[expected_name]
        if expected_overload_count != actual_overload_count:
            def create_decl(f: NativeFunction) -> str:
                with native_function_manager(f):
                    return DispatcherSignature.from_schema(f.func).decl()
            expected_schemas_str = '\n'.join([create_decl(f) for f in funcs])
            missing_kernels_err_msg += f"""
{class_name} is missing a kernel definition for {expected_name}. We found {actual_overload_count} kernel(s) with that name,
but expected {expected_overload_count} kernel(s). The expected function schemas for the missing operator are:
{expected_schemas_str}

"""
    assert missing_kernels_err_msg == "", missing_kernels_err_msg
