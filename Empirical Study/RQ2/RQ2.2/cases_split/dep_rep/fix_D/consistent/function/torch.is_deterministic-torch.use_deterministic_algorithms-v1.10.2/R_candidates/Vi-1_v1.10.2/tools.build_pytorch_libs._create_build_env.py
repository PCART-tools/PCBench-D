def _create_build_env() -> Dict[str, str]:
    # XXX - our cmake file sometimes looks at the system environment
    # and not cmake flags!
    # you should NEVER add something to this list. It is bad practice to
    # have cmake read the environment
    my_env = os.environ.copy()
    if 'CUDA_HOME' in my_env:  # Keep CUDA_HOME. This env variable is still used in other part.
        my_env['CUDA_BIN_PATH'] = my_env['CUDA_HOME']
    elif IS_WINDOWS:  # we should eventually make this as part of FindCUDA.
        cuda_win = glob('C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v*.*')
        if len(cuda_win) > 0:
            my_env['CUDA_BIN_PATH'] = cuda_win[0]

    if IS_WINDOWS and USE_NINJA:
        # When using Ninja under Windows, the gcc toolchain will be chosen as
        # default. But it should be set to MSVC as the user's first choice.
        my_env = _overlay_windows_vcvars(my_env)
        my_env.setdefault('CC', 'cl')
        my_env.setdefault('CXX', 'cl')
    return my_env
