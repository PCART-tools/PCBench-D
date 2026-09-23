def get_cpp_compiler() -> str:
    if _IS_WINDOWS:
        compiler = os.environ.get("CXX", "cl")
        check_compiler_exist_windows(compiler)
    else:
        if config.is_fbcode():
            return build_paths.cc
        if isinstance(config.cpp.cxx, (list, tuple)):
            search = tuple(config.cpp.cxx)
        else:
            search = (config.cpp.cxx,)
        compiler = cpp_compiler_search(search)
    return compiler
