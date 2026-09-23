@contextmanager
def _test_mode() -> Generator[None, None, None]:
    """
    Forces ``is_symm_mem_enabled_for_group()`` to return ``True`` and the ops
    defined in the ``symm_mem`` namespace to use fallback implementations.

    The context manager is not thread safe.
    """
    global _is_test_mode
    prev = _is_test_mode
    try:
        _is_test_mode = True
        yield
    finally:
        _is_test_mode = prev
