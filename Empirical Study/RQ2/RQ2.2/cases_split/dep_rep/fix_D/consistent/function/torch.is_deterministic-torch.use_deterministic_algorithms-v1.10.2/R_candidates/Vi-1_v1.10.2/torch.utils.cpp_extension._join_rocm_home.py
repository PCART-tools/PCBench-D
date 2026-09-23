def _join_rocm_home(*paths) -> str:
    r'''
    Joins paths with ROCM_HOME, or raises an error if it ROCM_HOME is not set.

    This is basically a lazy way of raising an error for missing $ROCM_HOME
    only once we need to get any ROCm-specific path.
    '''
    if ROCM_HOME is None:
        raise EnvironmentError('ROCM_HOME environment variable is not set. '
                               'Please set it to your ROCm install root.')
    elif IS_WINDOWS:
        raise EnvironmentError('Building PyTorch extensions using '
                               'ROCm and Windows is not supported.')
    return os.path.join(ROCM_HOME, *paths)
