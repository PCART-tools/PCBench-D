def _check_cusparse_spgemm_available():
    # cusparseSpGEMM was added in 11.0
    version = _get_torch_cuda_version()
    min_supported_version = (11, 0)
    return version >= min_supported_version
