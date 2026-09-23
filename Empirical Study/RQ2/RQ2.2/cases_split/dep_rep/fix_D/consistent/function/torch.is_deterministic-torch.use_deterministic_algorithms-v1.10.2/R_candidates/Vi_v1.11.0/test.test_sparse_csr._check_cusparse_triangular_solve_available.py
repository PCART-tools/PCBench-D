def _check_cusparse_triangular_solve_available():
    version = _get_torch_cuda_version()
    # cusparseSpSM was added in 11.3.1 but we don't have access to patch version
    min_supported_version = (11, 4)
    return version >= min_supported_version
