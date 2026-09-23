def _is_empty_method(func: SeriesMethod) -> bool:
    """
    Confirm that the given function has no implementation.

    Definitions of empty:

    - only has a docstring (body is empty)
    - has no docstring and just contains 'pass' (or equivalent)
    """
    fc = func.__code__
    return (fc.co_code in _EMPTY_BYTECODE) and (
        (len(fc.co_consts) == 2 and fc.co_consts[1] is None)
        # account for optimized-out docstrings (eg: running 'python -OO')
        or (sys.flags.optimize == 2 and fc.co_consts == (None,))
    )
