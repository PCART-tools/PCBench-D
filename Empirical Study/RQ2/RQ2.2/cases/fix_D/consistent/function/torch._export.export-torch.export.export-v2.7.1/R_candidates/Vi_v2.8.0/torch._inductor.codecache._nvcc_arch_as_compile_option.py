def _nvcc_arch_as_compile_option() -> str:
    arch = cuda_env.get_cuda_arch()
    if arch == "90":
        # Required by cutlass compilation.
        return "90a"
    if arch == "100":
        return "100a"
    return arch
