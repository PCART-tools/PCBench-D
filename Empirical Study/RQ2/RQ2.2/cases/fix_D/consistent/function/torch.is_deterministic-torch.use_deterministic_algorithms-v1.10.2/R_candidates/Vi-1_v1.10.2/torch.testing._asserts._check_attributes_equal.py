def _check_attributes_equal(
    actual: Tensor,
    expected: Tensor,
    *,
    check_device: bool = True,
    check_dtype: bool = True,
    check_stride: bool = True,
    check_is_coalesced: bool = True,
) -> Optional[_TestingErrorMeta]:
    """Checks if the attributes of two tensors match.

    Always checks the :attr:`~torch.Tensor.shape` and :attr:`~torch.Tensor.layout`. Checks for
    :attr:`~torch.Tensor.device`, :attr:`~torch.Tensor.dtype`, :meth:`~torch.Tensor.stride` if the tensors are strided,
    and :meth:`~torch.tensor.is_coalesced` if the tensors are sparse COO are optional and can be disabled.

    Args:
        actual (Tensor): Actual tensor.
        expected (Tensor): Expected tensor.
        check_device (bool): If ``True`` (default), checks that both :attr:`actual` and :attr:`expected` are on the
            same :attr:`~torch.Tensor.device`.
        check_dtype (bool): If ``True`` (default), checks that both :attr:`actual` and :attr:`expected` have the same
            ``dtype``.
        check_stride (bool): If ``True`` (default) and the tensors are strided, checks that both :attr:`actual` and
            :attr:`expected` have the same stride.
        check_is_coalesced (bool): If ``True`` (default) and the tensors are sparse COO, checks that both
            :attr:`actual` and :attr:`expected` are either coalesced or uncoalesced.

    Returns:
        (Optional[_TestingErrorMeta]): If checks did not pass.
    """
    msg_fmtstr = "The values for attribute '{}' do not match: {} != {}."

    if actual.shape != expected.shape:
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("shape", actual.shape, expected.shape))

    if actual.layout != expected.layout:
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("layout", actual.layout, expected.layout))
    elif actual.layout == torch.strided and check_stride and actual.stride() != expected.stride():
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("stride()", actual.stride(), expected.stride()))
    elif actual.layout == torch.sparse_coo and check_is_coalesced and actual.is_coalesced() != expected.is_coalesced():
        return _TestingErrorMeta(
            AssertionError, msg_fmtstr.format("is_coalesced()", actual.is_coalesced(), expected.is_coalesced())
        )

    if check_device and actual.device != expected.device:
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("device", actual.device, expected.device))

    if actual.is_quantized != expected.is_quantized:
        return _TestingErrorMeta(
            AssertionError, msg_fmtstr.format("is_quantized", actual.is_quantized, expected.is_quantized)
        )
    elif actual.is_quantized and actual.qscheme() != expected.qscheme():
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("qscheme()", actual.qscheme(), expected.qscheme()))

    if check_dtype and actual.dtype != expected.dtype:
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("dtype", actual.dtype, expected.dtype))

    return None
