def build_caffe2(
    version: Optional[str],
    cmake_python_library: Optional[str],
    build_python: bool,
    rerun_cmake: bool,
    cmake_only: bool,
    cmake: CMake,
) -> None:
    my_env = _create_build_env()
    build_test = not check_negative_env_flag('BUILD_TEST')
    cmake.generate(version,
                   cmake_python_library,
                   build_python,
                   build_test,
                   my_env,
                   rerun_cmake)
    if cmake_only:
        return
    cmake.build(my_env)
    if build_python:
        caffe2_proto_dir = os.path.join(cmake.build_dir, 'caffe2', 'proto')
        for proto_file in glob(os.path.join(caffe2_proto_dir, '*.py')):
            if proto_file != os.path.join(caffe2_proto_dir, '__init__.py'):
                shutil.copy(proto_file, os.path.join('caffe2', 'proto'))
