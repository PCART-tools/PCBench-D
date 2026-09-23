def _check_tensors_close(
    actual: Tensor,
    expected: Tensor,
    *,
    rtol: Optional[float] = None,
    atol: Optional[float] = None,
    equal_nan: bool = False,
    check_device: bool = True,
    check_dtype: bool = True,
    check_stride: bool = True,
    check_is_coalesced: bool = True,
    msg: Union[str, Callable[[Tensor, Tensor, Diagnostics], str]],
) -> Optional[_TestingErrorMeta]:
    r"""Checks that the values of :attr:`actual` and :attr:`expected` are close.

    If :attr:`actual` and :attr:`expected` are real-valued and finite, they are considered close if

    .. code::

        torch.abs(actual - expected) <= (atol + rtol * expected)

    and they have the same device (if :attr:`check_device` is ``True``), same dtype (if :attr:`check_dtype` is
    ``True``), and the same stride (if :attr:`check_stride` is ``True``). Non-finite values (``-inf`` and ``inf``) are
    only considered close if and only if they are equal. ``NaN``'s are only considered equal to each other if
    :attr:`equal_nan` is ``True``.

    For a description of the parameters see :func:`assert_close`.

    Returns:
        Optional[_TestingErrorMeta]: If checks did not pass.
    """
    if rtol is None or atol is None:
        rtol, atol = _get_default_rtol_and_atol(actual, expected)

    error_meta = _check_attributes_equal(
        actual,
        expected,
        check_device=check_device,
        check_dtype=check_dtype,
        check_stride=check_stride,
        check_is_coalesced=check_is_coalesced,
    )
    if error_meta:
        return error_meta
    actual, expected = _equalize_attributes(actual, expected)

    if rtol is None or atol is None:
        rtol, atol = _DTYPE_PRECISIONS.get(actual.dtype, (0.0, 0.0))

    error_meta = _check_values_close(actual, expected, rtol=rtol, atol=atol, equal_nan=equal_nan, msg=msg)
    if error_meta:
        return error_meta

    return None
