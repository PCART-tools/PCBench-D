def _check_cusparse_generic_available():
    version = _get_torch_cuda_version()
    min_supported_version = (10, 1)
    if IS_WINDOWS:
        min_supported_version = (11, 0)
    return version >= min_supported_version
