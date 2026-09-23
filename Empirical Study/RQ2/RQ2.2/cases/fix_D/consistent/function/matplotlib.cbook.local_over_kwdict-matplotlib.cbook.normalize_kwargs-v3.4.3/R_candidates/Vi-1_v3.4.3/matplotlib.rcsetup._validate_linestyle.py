def _validate_linestyle(ls):
    """
    A validator for all possible line styles, the named ones *and*
    the on-off ink sequences.
    """
    if isinstance(ls, str):
        try:  # Look first for a valid named line style, like '--' or 'solid'.
            return _validate_named_linestyle(ls)
        except ValueError:
            pass
        try:
            ls = ast.literal_eval(ls)  # Parsing matplotlibrc.
        except (SyntaxError, ValueError):
            pass  # Will error with the ValueError at the end.

    def _is_iterable_not_string_like(x):
        # Explicitly exclude bytes/bytearrays so that they are not
        # nonsensically interpreted as sequences of numbers (codepoints).
        return np.iterable(x) and not isinstance(x, (str, bytes, bytearray))

    # (offset, (on, off, on, off, ...))
    if (_is_iterable_not_string_like(ls)
            and len(ls) == 2
            and isinstance(ls[0], (type(None), Number))
            and _is_iterable_not_string_like(ls[1])
            and len(ls[1]) % 2 == 0
            and all(isinstance(elem, Number) for elem in ls[1])):
        if ls[0] is None:
            _api.warn_deprecated(
                "3.3", message="Passing the dash offset as None is deprecated "
                "since %(since)s and support for it will be removed "
                "%(removal)s; pass it as zero instead.")
            ls = (0, ls[1])
        return ls
    # For backcompat: (on, off, on, off, ...); the offset is implicitly None.
    if (_is_iterable_not_string_like(ls)
            and len(ls) % 2 == 0
            and all(isinstance(elem, Number) for elem in ls)):
        return (0, ls)
    raise ValueError(f"linestyle {ls!r} is not a valid on-off ink sequence.")
