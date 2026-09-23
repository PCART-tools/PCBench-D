@functools.lru_cache(None)
def is_clang() -> bool:
    return _is_clang(get_cpp_compiler())
