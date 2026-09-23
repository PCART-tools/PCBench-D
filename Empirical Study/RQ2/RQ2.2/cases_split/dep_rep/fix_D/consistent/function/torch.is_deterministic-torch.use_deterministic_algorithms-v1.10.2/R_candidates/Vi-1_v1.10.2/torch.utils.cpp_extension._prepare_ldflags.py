def _prepare_ldflags(extra_ldflags, with_cuda, verbose, is_standalone):
    if IS_WINDOWS:
        python_path = os.path.dirname(sys.executable)
        python_lib_path = os.path.join(python_path, 'libs')

        extra_ldflags.append('c10.lib')
        if with_cuda:
            extra_ldflags.append('c10_cuda.lib')
        extra_ldflags.append('torch_cpu.lib')
        if BUILD_SPLIT_CUDA and with_cuda:
            extra_ldflags.append('torch_cuda_cu.lib')
            # /INCLUDE is used to ensure torch_cuda_cu is linked against in a project that relies on it.
            extra_ldflags.append('-INCLUDE:?searchsorted_cuda@native@at@@YA?AVTensor@2@AEBV32@0_N1@Z')
            extra_ldflags.append('torch_cuda_cpp.lib')
            # /INCLUDE is used to ensure torch_cuda_cpp is linked against in a project that relies on it.
            # Related issue: https://github.com/pytorch/pytorch/issues/31611
            extra_ldflags.append('-INCLUDE:?warp_size@cuda@at@@YAHXZ')
        elif with_cuda:
            extra_ldflags.append('torch_cuda.lib')
            # /INCLUDE is used to ensure torch_cuda is linked against in a project that relies on it.
            # Related issue: https://github.com/pytorch/pytorch/issues/31611
            extra_ldflags.append('-INCLUDE:?warp_size@cuda@at@@YAHXZ')
        extra_ldflags.append('torch.lib')
        extra_ldflags.append(f'/LIBPATH:{TORCH_LIB_PATH}')
        if not is_standalone:
            extra_ldflags.append('torch_python.lib')
            extra_ldflags.append(f'/LIBPATH:{python_lib_path}')

    else:
        extra_ldflags.append(f'-L{TORCH_LIB_PATH}')
        extra_ldflags.append('-lc10')
        if with_cuda:
            extra_ldflags.append('-lc10_hip' if IS_HIP_EXTENSION else '-lc10_cuda')
        extra_ldflags.append('-ltorch_cpu')
        if BUILD_SPLIT_CUDA and with_cuda:
            extra_ldflags.append('-ltorch_hip' if IS_HIP_EXTENSION else '-ltorch_cuda_cu -ltorch_cuda_cpp')
        elif with_cuda:
            extra_ldflags.append('-ltorch_hip' if IS_HIP_EXTENSION else '-ltorch_cuda')
        extra_ldflags.append('-ltorch')
        if not is_standalone:
            extra_ldflags.append('-ltorch_python')

        if is_standalone and "TBB" in torch.__config__.parallel_info():
            extra_ldflags.append('-ltbb')

        if is_standalone:
            extra_ldflags.append(f"-Wl,-rpath,{TORCH_LIB_PATH}")

    if with_cuda:
        if verbose:
            print('Detected CUDA files, patching ldflags')
        if IS_WINDOWS:
            extra_ldflags.append(f'/LIBPATH:{_join_cuda_home("lib/x64")}')
            extra_ldflags.append('cudart.lib')
            if CUDNN_HOME is not None:
                extra_ldflags.append(os.path.join(CUDNN_HOME, 'lib/x64'))
        elif not IS_HIP_EXTENSION:
            extra_ldflags.append(f'-L{_join_cuda_home("lib64")}')
            extra_ldflags.append('-lcudart')
            if CUDNN_HOME is not None:
                extra_ldflags.append(f'-L{os.path.join(CUDNN_HOME, "lib64")}')
        elif IS_HIP_EXTENSION:
            assert ROCM_VERSION is not None
            extra_ldflags.append(f'-L{_join_rocm_home("lib")}')
            extra_ldflags.append('-lamdhip64' if ROCM_VERSION >= (3, 5) else '-lhip_hcc')
    return extra_ldflags
