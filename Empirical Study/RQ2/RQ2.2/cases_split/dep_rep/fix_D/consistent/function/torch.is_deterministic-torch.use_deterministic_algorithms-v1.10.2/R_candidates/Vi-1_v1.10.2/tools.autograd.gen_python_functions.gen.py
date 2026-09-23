def gen(out: str, native_yaml_path: str, deprecated_yaml_path: str, template_path: str) -> None:
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    native_functions = parse_native_yaml(native_yaml_path).native_functions
    native_functions = list(filter(should_generate_py_binding, native_functions))

    methods = load_signatures(native_functions, deprecated_yaml_path, method=True)
    create_python_bindings(
        fm, methods, is_py_variable_method, None, 'python_variable_methods.cpp', method=True)

    # NOTE: num_shards here must be synced with gatherTorchFunctions in
    #       torch/csrc/autograd/python_torch_functions_manual.cpp
    functions = load_signatures(native_functions, deprecated_yaml_path, method=False)
    create_python_bindings_sharded(
        fm, functions, is_py_torch_function, 'torch', 'python_torch_functions.cpp',
        method=False, num_shards=3)

    create_python_bindings(
        fm, functions, is_py_nn_function, 'torch.nn', 'python_nn_functions.cpp', method=False)

    create_python_bindings(
        fm, functions, is_py_fft_function, 'torch.fft', 'python_fft_functions.cpp', method=False)

    create_python_bindings(
        fm, functions, is_py_linalg_function, 'torch.linalg', 'python_linalg_functions.cpp', method=False)

    create_python_bindings(
        fm, functions, is_py_special_function, 'torch.special', 'python_special_functions.cpp', method=False)
