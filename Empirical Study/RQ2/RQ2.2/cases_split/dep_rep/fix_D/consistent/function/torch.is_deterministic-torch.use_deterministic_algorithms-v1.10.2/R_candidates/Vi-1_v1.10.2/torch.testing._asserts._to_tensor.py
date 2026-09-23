def _to_tensor(tensor_or_scalar_like: Any) -> Tuple[Optional[_TestingErrorMeta], Optional[Tensor]]:
    """Converts a tensor-or-scalar-like to a :class:`~torch.Tensor`.
    Args:
        tensor_or_scalar_like (Any): Tensor-or-scalar-like.
    Returns:

        (Tuple[Optional[_TestingErrorMeta], Optional[Tensor]]): The two elements are orthogonal, i.e. if the first is
            ``None`` the second will be valid and vice versa. Returns :class:`_TestingErrorMeta` if no tensor can be
            constructed from :attr:`actual` or :attr:`expected`. Additionally, returns any error meta from
            :func:`_check_supported_tensor`.
    """
    error_meta: Optional[_TestingErrorMeta]

    if isinstance(tensor_or_scalar_like, Tensor):
        tensor = tensor_or_scalar_like
    else:
        try:
            tensor = torch.as_tensor(tensor_or_scalar_like)
        except Exception:
            error_meta = _TestingErrorMeta(
                ValueError, f"No tensor can be constructed from type {type(tensor_or_scalar_like)}."
            )
            return error_meta, None

    error_meta = _check_supported_tensor(tensor)
    if error_meta:
        return error_meta, None

    return None, tensor
