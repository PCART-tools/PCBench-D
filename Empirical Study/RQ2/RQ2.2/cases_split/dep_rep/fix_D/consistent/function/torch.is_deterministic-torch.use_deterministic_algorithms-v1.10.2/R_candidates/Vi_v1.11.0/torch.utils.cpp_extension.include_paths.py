def include_paths(cuda: bool = False) -> List[str]:
    '''
    Get the include paths required to build a C++ or CUDA extension.

    Args:
        cuda: If `True`, includes CUDA-specific include paths.

    Returns:
        A list of include path strings.
    '''
    lib_include = os.path.join(_TORCH_PATH, 'include')
    paths = [
        lib_include,
        # Remove this once torch/torch.h is officially no longer supported for C++ extensions.
        os.path.join(lib_include, 'torch', 'csrc', 'api', 'include'),
        # Some internal (old) Torch headers don't properly prefix their includes,
        # so we need to pass -Itorch/lib/include/TH as well.
        os.path.join(lib_include, 'TH'),
        os.path.join(lib_include, 'THC')
    ]
    if cuda and IS_HIP_EXTENSION:
        paths.append(os.path.join(lib_include, 'THH'))
        paths.append(_join_rocm_home('include'))
        if MIOPEN_HOME is not None:
            paths.append(os.path.join(MIOPEN_HOME, 'include'))
    elif cuda:
        cuda_home_include = _join_cuda_home('include')
        # if we have the Debian/Ubuntu packages for cuda, we get /usr as cuda home.
        # but gcc doesn't like having /usr/include passed explicitly
        if cuda_home_include != '/usr/include':
            paths.append(cuda_home_include)
        if CUDNN_HOME is not None:
            paths.append(os.path.join(CUDNN_HOME, 'include'))
    return paths
