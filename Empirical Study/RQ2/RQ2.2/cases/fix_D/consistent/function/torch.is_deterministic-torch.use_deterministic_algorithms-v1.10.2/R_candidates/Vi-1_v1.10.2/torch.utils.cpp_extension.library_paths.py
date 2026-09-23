def library_paths(cuda: bool = False) -> List[str]:
    r'''
    Get the library paths required to build a C++ or CUDA extension.

    Args:
        cuda: If `True`, includes CUDA-specific library paths.

    Returns:
        A list of library path strings.
    '''
    # We need to link against libtorch.so
    paths = [TORCH_LIB_PATH]

    if cuda and IS_HIP_EXTENSION:
        lib_dir = 'lib'
        paths.append(_join_rocm_home(lib_dir))
    elif cuda:
        if IS_WINDOWS:
            lib_dir = 'lib/x64'
        else:
            lib_dir = 'lib64'
            if (not os.path.exists(_join_cuda_home(lib_dir)) and
                    os.path.exists(_join_cuda_home('lib'))):
                # 64-bit CUDA may be installed in 'lib' (see e.g. gh-16955)
                # Note that it's also possible both don't exist (see
                # _find_cuda_home) - in that case we stay with 'lib64'.
                lib_dir = 'lib'

        paths.append(_join_cuda_home(lib_dir))
        if CUDNN_HOME is not None:
            paths.append(os.path.join(CUDNN_HOME, lib_dir))
    return paths
