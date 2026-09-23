def to_test_backend_selective(module, method_compile_spec, submodules):
    def _to_test_backend(module):
        return to_test_backend(module, method_compile_spec)

    return torch._C._jit_to_backend_selective(module, _to_test_backend, submodules)
