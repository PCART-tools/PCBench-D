def _get_shared_cflag(compile_only: bool) -> list[str]:
    if _IS_WINDOWS:
        """
        MSVC `/MD` using python `ucrtbase.dll` lib as runtime.
        https://learn.microsoft.com/en-us/cpp/c-runtime-library/crt-library-features?view=msvc-170
        """
        SHARED_FLAG = ["DLL", "MD"]
    else:
        if compile_only:
            return ["fPIC"]
        if platform.system() == "Darwin" and "clang" in get_cpp_compiler():
            # This causes undefined symbols to behave the same as linux
            return ["shared", "fPIC", "undefined dynamic_lookup"]
        else:
            return ["shared", "fPIC"]

    return SHARED_FLAG
