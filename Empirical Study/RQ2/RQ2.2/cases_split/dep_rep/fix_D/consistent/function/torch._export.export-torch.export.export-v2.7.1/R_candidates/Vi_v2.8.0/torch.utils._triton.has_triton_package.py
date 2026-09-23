@functools.cache
def has_triton_package() -> bool:
    try:
        from triton.compiler.compiler import triton_key

        return triton_key is not None
    except ImportError:
        return False
    except RuntimeError:
        return False
