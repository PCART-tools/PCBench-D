def get_py_torch_functions(
        python_funcs: Sequence[PythonSignatureNativeFunctionPair],
        method: bool = False,
) -> Sequence[PythonSignatureGroup]:
    """
    Get declarations (grouped by name) which should be generated
    as either functions in the "torch" module or methods on Tensor.
    """
    def should_bind_function(python_func: PythonSignatureNativeFunctionPair) -> bool:
        return (should_generate_py_binding(python_func.function) and
                not python_func.function.python_module and
                Variant.function in python_func.function.variants)

    def should_bind_method(python_func: PythonSignatureNativeFunctionPair) -> bool:
        return (should_generate_py_binding(python_func.function) and
                not python_func.function.python_module and
                Variant.method in python_func.function.variants)

    should_bind = should_bind_method if method else should_bind_function
    return group_overloads([f for f in python_funcs if should_bind(f)])
