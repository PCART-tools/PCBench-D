def _write_ninja_file_to_build_library(path,
                                       name,
                                       sources,
                                       extra_cflags,
                                       extra_cuda_cflags,
                                       extra_ldflags,
                                       extra_include_paths,
                                       with_cuda,
                                       is_standalone) -> None:
    extra_cflags = [flag.strip() for flag in extra_cflags]
    extra_cuda_cflags = [flag.strip() for flag in extra_cuda_cflags]
    extra_ldflags = [flag.strip() for flag in extra_ldflags]
    extra_include_paths = [flag.strip() for flag in extra_include_paths]

    # Turn into absolute paths so we can emit them into the ninja build
    # file wherever it is.
    user_includes = [os.path.abspath(file) for file in extra_include_paths]

    # include_paths() gives us the location of torch/extension.h
    system_includes = include_paths(with_cuda)
    # sysconfig.get_path('include') gives us the location of Python.h
    # Explicitly specify 'posix_prefix' scheme on non-Windows platforms to workaround error on some MacOS
    # installations where default `get_path` points to non-existing `/Library/Python/M.m/include` folder
    python_include_path = sysconfig.get_path('include', scheme='nt' if IS_WINDOWS else 'posix_prefix')
    if python_include_path is not None:
        system_includes.append(python_include_path)

    # Windows does not understand `-isystem`.
    if IS_WINDOWS:
        user_includes += system_includes
        system_includes.clear()

    common_cflags = []
    if not is_standalone:
        common_cflags.append(f'-DTORCH_EXTENSION_NAME={name}')
        common_cflags.append('-DTORCH_API_INCLUDE_EXTENSION_H')

    # Note [Pybind11 ABI constants]
    #
    # Pybind11 before 2.4 used to build an ABI strings using the following pattern:
    # f"__pybind11_internals_v{PYBIND11_INTERNALS_VERSION}{PYBIND11_INTERNALS_KIND}{PYBIND11_BUILD_TYPE}__"
    # Since 2.4 compier type, stdlib and build abi parameters are also encoded like this:
    # f"__pybind11_internals_v{PYBIND11_INTERNALS_VERSION}{PYBIND11_INTERNALS_KIND}{PYBIND11_COMPILER_TYPE}{PYBIND11_STDLIB}{PYBIND11_BUILD_ABI}{PYBIND11_BUILD_TYPE}__"
    #
    # This was done in order to further narrow down the chances of compiler ABI incompatibility
    # that can cause a hard to debug segfaults.
    # For PyTorch extensions we want to relax those restrictions and pass compiler, stdlib and abi properties
    # captured during PyTorch native library compilation in torch/csrc/Module.cpp

    for pname in ["COMPILER_TYPE", "STDLIB", "BUILD_ABI"]:
        pval = getattr(torch._C, f"_PYBIND11_{pname}")
        if pval is not None and not IS_WINDOWS:
            common_cflags.append(f'-DPYBIND11_{pname}=\\"{pval}\\"')

    common_cflags += [f'-I{include}' for include in user_includes]
    common_cflags += [f'-isystem {include}' for include in system_includes]

    common_cflags += ['-D_GLIBCXX_USE_CXX11_ABI=' + str(int(torch._C._GLIBCXX_USE_CXX11_ABI))]

    if IS_WINDOWS:
        cflags = common_cflags + COMMON_MSVC_FLAGS + extra_cflags
        cflags = _nt_quote_args(cflags)
    else:
        cflags = common_cflags + ['-fPIC', '-std=c++14'] + extra_cflags

    if with_cuda and IS_HIP_EXTENSION:
        cuda_flags = ['-DWITH_HIP'] + cflags + COMMON_HIP_FLAGS + COMMON_HIPCC_FLAGS
        cuda_flags += extra_cuda_cflags
        cuda_flags += _get_rocm_arch_flags(cuda_flags)
        sources = [s if not _is_cuda_file(s) else
                   os.path.abspath(os.path.join(
                       path, get_hip_file_path(os.path.relpath(s, path), is_pytorch_extension=True)))
                   for s in sources]
    elif with_cuda:
        cuda_flags = common_cflags + COMMON_NVCC_FLAGS + _get_cuda_arch_flags()
        if IS_WINDOWS:
            for flag in COMMON_MSVC_FLAGS:
                cuda_flags = ['-Xcompiler', flag] + cuda_flags
            for ignore_warning in MSVC_IGNORE_CUDAFE_WARNINGS:
                cuda_flags = ['-Xcudafe', '--diag_suppress=' + ignore_warning] + cuda_flags
            cuda_flags = _nt_quote_args(cuda_flags)
            cuda_flags += _nt_quote_args(extra_cuda_cflags)
        else:
            cuda_flags += ['--compiler-options', "'-fPIC'"]
            cuda_flags += extra_cuda_cflags
            if not any(flag.startswith('-std=') for flag in cuda_flags):
                cuda_flags.append('-std=c++14')
            if os.getenv("CC") is not None:
                cuda_flags = ['-ccbin', os.getenv("CC")] + cuda_flags
    else:
        cuda_flags = None

    def object_file_path(source_file: str) -> str:
        # '/path/to/file.cpp' -> 'file'
        file_name = os.path.splitext(os.path.basename(source_file))[0]
        if _is_cuda_file(source_file) and with_cuda:
            # Use a different object filename in case a C++ and CUDA file have
            # the same filename but different extension (.cpp vs. .cu).
            target = f'{file_name}.cuda.o'
        else:
            target = f'{file_name}.o'
        return target

    objects = [object_file_path(src) for src in sources]
    ldflags = ([] if is_standalone else [SHARED_FLAG]) + extra_ldflags

    # The darwin linker needs explicit consent to ignore unresolved symbols.
    if IS_MACOS:
        ldflags.append('-undefined dynamic_lookup')
    elif IS_WINDOWS:
        ldflags = _nt_quote_args(ldflags)

    ext = EXEC_EXT if is_standalone else LIB_EXT
    library_target = f'{name}{ext}'

    _write_ninja_file(
        path=path,
        cflags=cflags,
        post_cflags=None,
        cuda_cflags=cuda_flags,
        cuda_post_cflags=None,
        sources=sources,
        objects=objects,
        ldflags=ldflags,
        library_target=library_target,
        with_cuda=with_cuda)
