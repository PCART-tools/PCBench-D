def log_softmax(input: Tensor, dim: int, dtype: Optional[DType] = None) -> Tensor:
    r"""Applies a softmax function followed by logarithm.

    See :class:`~torch.sparse.softmax` for more details.

    Args:
        input (Tensor): input
        dim (int): A dimension along which softmax will be computed.
        dtype (:class:`torch.dtype`, optional): the desired data type
          of returned tensor.  If specified, the input tensor is
          casted to :attr:`dtype` before the operation is
          performed. This is useful for preventing data type
          overflows. Default: None
    """
    return torch._sparse_log_softmax(input, dim, dtype=dtype)
