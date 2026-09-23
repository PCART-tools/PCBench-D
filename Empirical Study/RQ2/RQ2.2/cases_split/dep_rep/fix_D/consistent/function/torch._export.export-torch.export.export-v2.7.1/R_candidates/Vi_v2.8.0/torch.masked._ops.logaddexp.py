def logaddexp(
    input: Union[Tensor, MaskedTensor],
    other: Union[Tensor, MaskedTensor],
    *,
    dtype: Optional[DType] = None,
    input_mask: Optional[Tensor] = None,
    other_mask: Optional[Tensor] = None,
) -> Tensor:
    """logaddexp(input, other, *, dtype=None, input_mask=None, other_mask=None) -> Tensor

    Returns logaddexp of all the elements in the :attr:`input` and the :attr:`other`
    tensor. The :attr:`input` elements are masked out according to the boolean tensor
    :attr:`input_mask` and the attr:`other` elements are masked out according to the boolean tensor
    :attr:`other_mask`.

    The shapes of a mask tensor and the tensor to be masked
    don't need to match, but they must be :ref:`broadcastable
    <broadcasting-semantics>` and the dimensionality of the mask
    tensor must not be greater than of the tensor to be masked.

    Args:
        input (Tensor): the input tensor
        other (Tensor): the second input tensor

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type
          of returned tensor.  If specified, the output tensor is
          casted to :attr:`dtype` after the operation is
          performed. Default: None.
        input_mask (:class:`torch.Tensor`, optional): the boolean tensor
          containing the binary mask of validity of :attr:`input` tensor elements.
          Default: None that is equivalent to ``torch.ones(input.shape, dtype=torch.bool)``.
        other_mask (:class:`torch.Tensor`, optional): the boolean tensor
          containing the binary mask of validity of :attr:`other` tensor elements.
          Default: None that is equivalent to ``torch.ones(other.shape, dtype=torch.bool)``.

    Example::

        >>> input = torch.tensor([-100.0, -200, -300])
        >>> input
        tensor([-100., -200., -300.])
        >>> other = torch.tensor([-1.0, -2, -3])
        >>> other
        tensor([-1., -2., -3.])
        >>> mask = torch.tensor([True, False, True])
        >>> mask
        tensor([ True, False,  True])
        >>> torch.masked._ops.logaddexp(input, other, input_mask=mask, other_mask=mask)
        tensor([-1., -inf, -3.])"""
    if dtype is None:
        dtype = input.dtype
    if input.layout == torch.strided and other.layout == torch.strided:
        mask_input = _combine_input_and_mask(logaddexp, input, input_mask)
        mask_other = _combine_input_and_mask(logaddexp, other, other_mask)
        return torch.logaddexp(mask_input, mask_other).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked logaddexp expects strided tensors (got {input.layout} tensor for input, {other.layout} for other)"
        )
