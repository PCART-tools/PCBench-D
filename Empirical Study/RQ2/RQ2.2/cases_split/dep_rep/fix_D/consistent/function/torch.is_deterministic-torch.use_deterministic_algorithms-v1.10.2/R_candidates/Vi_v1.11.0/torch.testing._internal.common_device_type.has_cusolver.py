def has_cusolver():
    version = _get_torch_cuda_version()
    # cuSolver is disabled on cuda < 10.1.243
    return version >= (10, 2)
