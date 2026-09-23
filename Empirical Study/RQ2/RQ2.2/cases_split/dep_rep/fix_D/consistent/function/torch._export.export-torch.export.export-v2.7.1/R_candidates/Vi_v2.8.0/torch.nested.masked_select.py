def masked_select(tensor: Tensor, mask: Tensor) -> Tensor:
    r"""
    Constructs a nested tensor given a strided tensor input and a strided mask, the resulting jagged layout nested tensor
    will have values retain values where the mask is equal to True. The dimensionality of the mask is preserved and is
    represented with the offsets, this is unlike :func:`masked_select` where the output is collapsed to a 1D tensor.

    Args:
    tensor (:class:`torch.Tensor`): a strided tensor from which the jagged layout nested tensor is constructed from.
    mask (:class:`torch.Tensor`): a strided mask tensor which is applied to the tensor input

    Example::

        >>> tensor = torch.randn(3, 3)
        >>> mask = torch.tensor([[False, False, True], [True, False, True], [False, False, True]])
        >>> nt = torch.nested.masked_select(tensor, mask)
        >>> nt.shape
        torch.Size([3, j4])
        >>> # Length of each item in the batch:
        >>> nt.offsets().diff()
        tensor([1, 2, 1])

        >>> tensor = torch.randn(6, 5)
        >>> mask = torch.tensor([False])
        >>> nt = torch.nested.masked_select(tensor, mask)
        >>> nt.shape
        torch.Size([6, j5])
        >>> # Length of each item in the batch:
        >>> nt.offsets().diff()
        tensor([0, 0, 0, 0, 0, 0])
    """
    if tensor.layout != torch.strided:
        raise RuntimeError(
            f"torch.nested.masked_select requires a strided tensor, given {tensor.layout}"
        )

    if mask.layout != torch.strided:
        raise RuntimeError(
            f"torch.nested.masked_select requires a strided mask, given: {mask.layout}"
        )
    res_values = tensor.masked_select(mask)
    expanded_mask = mask.expand(tensor.shape)
    res_lengths = expanded_mask.sum(dim=tensor.ndim - 1).view(-1)

    from torch.nested._internal.nested_tensor import nested_view_from_values_offsets

    return nested_view_from_values_offsets(
        values=res_values,
        offsets=F.pad(res_lengths.cumsum(dim=0), (1, 0)),
    )
