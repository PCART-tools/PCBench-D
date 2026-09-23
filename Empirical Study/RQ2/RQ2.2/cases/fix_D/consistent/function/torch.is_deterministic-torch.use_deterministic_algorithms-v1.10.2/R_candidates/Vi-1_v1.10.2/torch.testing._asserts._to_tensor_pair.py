def _to_tensor_pair(
    actual: Any, expected: Any, *, allow_subclasses: bool
) -> Tuple[Optional[_TestingErrorMeta], Optional[_TensorPair]]:
    """Converts a tensor-or-scalar-like pair to a :class:`_TensorPair`.

    Args:
        actual (Any): Actual tensor-or-scalar-like.
        expected (Any): Expected tensor-or-scalar-like.
        allow_subclasses (bool): If ``True`` (default) and except for Python scalars, inputs of directly related types
            are allowed. Otherwise type equality is required.

    Returns:
        (Optional[_TestingErrorMeta], Optional[_TensorPair]): The two elements are orthogonal, i.e. if the first is
            ``None`` the second will not and vice versa. Returns :class:`_TestingErrorMeta` if :attr:`actual` and
            :attr:`expected` are not scalars and do not have the same type. Additionally, returns any error meta from
            :func:`_to_tensor`.
    """
    error_meta = _check_types(actual, expected, allow_subclasses=allow_subclasses)
    if error_meta:
        return error_meta, None

    error_meta, actual = _to_tensor(actual)
    if error_meta:
        return error_meta, None

    error_meta, expected = _to_tensor(expected)
    if error_meta:
        return error_meta, None

    return None, _TensorPair(actual, expected)
