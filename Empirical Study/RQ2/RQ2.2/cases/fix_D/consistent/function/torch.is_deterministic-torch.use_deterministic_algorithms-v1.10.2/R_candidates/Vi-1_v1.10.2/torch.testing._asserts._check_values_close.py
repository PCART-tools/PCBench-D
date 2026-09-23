@_check_quantized
@_check_sparse_coo_members_individually
@_check_sparse_csr_members_individually
def _check_values_close(
    actual: Tensor,
    expected: Tensor,
    *,
    rtol: float,
    atol: float,
    equal_nan: bool,
    msg: Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]],
) -> Optional[_TestingErrorMeta]:
    """Checks if the values of two tensors are close up to a desired tolerance.

    Args:
        actual (Tensor): Actual tensor.
        expected (Tensor): Expected tensor.
        rtol (float): Relative tolerance.
        atol (float): Absolute tolerance.
        equal_nan (bool): If ``True``, two ``NaN`` values will be considered equal.
        msg (Optional[Union[str, Callable[[Tensor, Tensor, Diagnostics], str]]]): Optional error message. Can be passed
            as callable in which case it will be called with the inputs and the result of :func:`_trace_mismatches`.

    Returns:
        (Optional[AssertionError]): If check did not pass.
    """
    dtype = _get_comparison_dtype(actual.dtype)
    actual = actual.to(dtype)
    expected = expected.to(dtype)
    mismatches = ~torch.isclose(actual, expected, rtol=rtol, atol=atol, equal_nan=equal_nan)
    if not torch.any(mismatches):
        return None

    diagnostics = _trace_mismatches(actual, expected, mismatches, rtol=rtol, atol=atol)
    if msg is None:
        msg = _make_mismatch_msg
    if callable(msg):
        msg = msg(actual, expected, diagnostics)
    return _TestingErrorMeta(AssertionError, msg)
