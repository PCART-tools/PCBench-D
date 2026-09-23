def to_test_backend_multi(module, method_compile_spec):
    return torch._C._jit_to_backend("test_backend", module, method_compile_spec)
