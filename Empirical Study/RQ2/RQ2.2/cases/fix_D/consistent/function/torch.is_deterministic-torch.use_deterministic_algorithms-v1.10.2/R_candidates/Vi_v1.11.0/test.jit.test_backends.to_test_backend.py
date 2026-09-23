def to_test_backend(module, method_compile_spec):
    return torch._C._jit_to_backend("test_backend", module, {"forward": method_compile_spec})
