def compile_cpp_code_inline(name, cpp_sources, functions):
    cpp_module = torch.utils.cpp_extension.load_inline(
        name=name,
        cpp_sources=cpp_sources,
        extra_cflags=['-g'],  # Enable debug symbols by default for debugging test failures.
        functions=functions,
        verbose=False,
    )
    return cpp_module
