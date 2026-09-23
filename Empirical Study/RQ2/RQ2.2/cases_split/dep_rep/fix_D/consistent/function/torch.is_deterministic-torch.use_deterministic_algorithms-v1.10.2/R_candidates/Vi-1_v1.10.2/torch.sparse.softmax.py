def softmax(input: Tensor, dim: int, dtype: Optional[DType] = None) -> Tensor:
    r"""Applies a softmax function.

    Softmax is defined as:

    :math:`\text{Softmax}(x_{i}) = \frac{exp(x_i)}{\sum_j exp(x_j)}`

    where :math:`i, j` run over sparse tensor indices and unspecified
    entries are ignores. This is equivalent to defining unspecified
    entries as negative infinity so that :math:`exp(x_k) = 0` when the
    entry with index :math:`k` has not specified.

    It is applied to all slices along `dim`, and will re-scale them so
    that the elements lie in the range `[0, 1]` and sum to 1.

    Args:
        input (Tensor): input
        dim (int): A dimension along which softmax will be computed.
        dtype (:class:`torch.dtype`, optional): the desired data type
          of returned tensor.  If specified, the input tensor is
          casted to :attr:`dtype` before the operation is
          performed. This is useful for preventing data type
          overflows. Default: None
    """
    return torch._sparse_softmax(input, dim, dtype=dtype)
