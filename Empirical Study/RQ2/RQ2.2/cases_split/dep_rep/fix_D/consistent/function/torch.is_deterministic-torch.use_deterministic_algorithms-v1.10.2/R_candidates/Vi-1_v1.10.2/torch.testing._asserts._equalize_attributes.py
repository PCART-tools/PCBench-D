def _equalize_attributes(actual: Tensor, expected: Tensor) -> Tuple[Tensor, Tensor]:
    """Equalizes some attributes of two tensors for value comparison.

    If :attr:`actual` and :attr:`expected`
    - are not on the same :attr:`~torch.Tensor.device`, they are moved CPU memory, and
    - do not have the same ``dtype``, they are promoted  to a common ``dtype`` (according to
        :func:`torch.promote_types`)

    Args:
        actual (Tensor): Actual tensor.
        expected (Tensor): Expected tensor.

    Returns:
        Tuple(Tensor, Tensor): Equalized tensors.
    """
    if actual.device != expected.device:
        actual = actual.cpu()
        expected = expected.cpu()

    if actual.dtype != expected.dtype:
        dtype = torch.promote_types(actual.dtype, expected.dtype)
        actual = actual.to(dtype)
        expected = expected.to(dtype)

    if actual.is_sparse and actual.is_coalesced() != expected.is_coalesced():
        actual = actual.coalesce()
        expected = expected.coalesce()

    return actual, expected
