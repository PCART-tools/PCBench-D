def _check_cusparse_sddmm_available():
    version = _get_torch_cuda_version()
    # cusparseSDDMM was added in 11.2.1 but we don't have access to patch version
    min_supported_version = (11, 3)
    return version >= min_supported_version
