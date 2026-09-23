def configure_extension_build():
    r"""Configures extension build options according to system environment and user's choice.

    Returns:
      The input to parameters ext_modules, cmdclass, packages, and entry_points as required in setuptools.setup.
    """

    try:
        cmake_cache_vars = defaultdict(lambda: False, cmake.get_cmake_cache_variables())
    except FileNotFoundError:
        # CMakeCache.txt does not exist. Probably running "python setup.py clean" over a clean directory.
        cmake_cache_vars = defaultdict(lambda: False)

    ################################################################################
    # Configure compile flags
    ################################################################################

    library_dirs = []
    extra_install_requires = []

    if IS_WINDOWS:
        # /NODEFAULTLIB makes sure we only link to DLL runtime
        # and matches the flags set for protobuf and ONNX
        extra_link_args = ['/NODEFAULTLIB:LIBCMT.LIB']
        # /MD links against DLL runtime
        # and matches the flags set for protobuf and ONNX
        # /EHsc is about standard C++ exception handling
        # /DNOMINMAX removes builtin min/max functions
        # /wdXXXX disables warning no. XXXX
        extra_compile_args = ['/MD', '/EHsc', '/DNOMINMAX',
                              '/wd4267', '/wd4251', '/wd4522', '/wd4522', '/wd4838',
                              '/wd4305', '/wd4244', '/wd4190', '/wd4101', '/wd4996',
                              '/wd4275']
    else:
        extra_link_args = []
        extra_compile_args = [
            '-Wall',
            '-Wextra',
            '-Wno-strict-overflow',
            '-Wno-unused-parameter',
            '-Wno-missing-field-initializers',
            '-Wno-write-strings',
            '-Wno-unknown-pragmas',
            # This is required for Python 2 declarations that are deprecated in 3.
            '-Wno-deprecated-declarations',
            # Python 2.6 requires -fno-strict-aliasing, see
            # http://legacy.python.org/dev/peps/pep-3123/
            # We also depend on it in our code (even Python 3).
            '-fno-strict-aliasing',
            # Clang has an unfixed bug leading to spurious missing
            # braces warnings, see
            # https://bugs.llvm.org/show_bug.cgi?id=21629
            '-Wno-missing-braces',
        ]

    library_dirs.append(lib_path)

    main_compile_args = []
    main_libraries = ['torch_python']
    main_link_args = []
    main_sources = ["torch/csrc/stub.c"]

    if cmake_cache_vars['USE_CUDA']:
        library_dirs.append(
            os.path.dirname(cmake_cache_vars['CUDA_CUDA_LIB']))

    if build_type.is_debug():
        if IS_WINDOWS:
            extra_compile_args.append('/Z7')
            extra_link_args.append('/DEBUG:FULL')
        else:
            extra_compile_args += ['-O0', '-g']
            extra_link_args += ['-O0', '-g']

    if build_type.is_rel_with_deb_info():
        if IS_WINDOWS:
            extra_compile_args.append('/Z7')
            extra_link_args.append('/DEBUG:FULL')
        else:
            extra_compile_args += ['-g']
            extra_link_args += ['-g']

    # Cross-compile for M1
    if IS_DARWIN:
        macos_target_arch = os.getenv('CMAKE_OSX_ARCHITECTURES', '')
        if macos_target_arch in ['arm64', 'x86_64']:
            macos_sysroot_path = os.getenv('CMAKE_OSX_SYSROOT')
            if macos_sysroot_path is None:
                macos_sysroot_path = subprocess.check_output([
                    'xcrun', '--show-sdk-path', '--sdk', 'macosx'
                ]).decode('utf-8').strip()
            extra_compile_args += ['-arch', macos_target_arch, '-isysroot', macos_sysroot_path]
            extra_link_args += ['-arch', macos_target_arch]


    def make_relative_rpath_args(path):
        if IS_DARWIN:
            return ['-Wl,-rpath,@loader_path/' + path]
        elif IS_WINDOWS:
            return []
        else:
            return ['-Wl,-rpath,$ORIGIN/' + path]

    ################################################################################
    # Declare extensions and package
    ################################################################################

    extensions = []
    packages = find_packages(exclude=('tools', 'tools.*'))
    C = Extension("torch._C",
                  libraries=main_libraries,
                  sources=main_sources,
                  language='c',
                  extra_compile_args=main_compile_args + extra_compile_args,
                  include_dirs=[],
                  library_dirs=library_dirs,
                  extra_link_args=extra_link_args + main_link_args + make_relative_rpath_args('lib'))
    extensions.append(C)

    if not IS_WINDOWS:
        DL = Extension("torch._dl",
                       sources=["torch/csrc/dl.c"],
                       language='c')
        extensions.append(DL)

    # These extensions are built by cmake and copied manually in build_extensions()
    # inside the build_ext implementation
    extensions.append(
        Extension(
            name=str('caffe2.python.caffe2_pybind11_state'),
            sources=[]),
    )
    if cmake_cache_vars['USE_CUDA']:
        extensions.append(
            Extension(
                name=str('caffe2.python.caffe2_pybind11_state_gpu'),
                sources=[]),
        )
    if cmake_cache_vars['USE_ROCM']:
        extensions.append(
            Extension(
                name=str('caffe2.python.caffe2_pybind11_state_hip'),
                sources=[]),
        )

    cmdclass = {
        'bdist_wheel': wheel_concatenate,
        'build_ext': build_ext,
        'clean': clean,
        'install': install,
        'sdist': sdist,
    }

    entry_points = {
        'console_scripts': [
            'convert-caffe2-to-onnx = caffe2.python.onnx.bin.conversion:caffe2_to_onnx',
            'convert-onnx-to-caffe2 = caffe2.python.onnx.bin.conversion:onnx_to_caffe2',
            'torchrun = torch.distributed.run:main',
        ]
    }

    return extensions, cmdclass, packages, entry_points, extra_install_requires
