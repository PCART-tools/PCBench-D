def gen_ops() -> list[Any]:
    """
    Generates all supported CUTLASS operations.
    """
    arch = get_cuda_arch()
    version = get_cuda_version()
    return _gen_ops_cached(arch, version)
