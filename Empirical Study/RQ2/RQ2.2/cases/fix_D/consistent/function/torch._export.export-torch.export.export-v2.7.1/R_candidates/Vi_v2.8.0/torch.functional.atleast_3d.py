def atleast_3d(*tensors):
    r"""
    Returns a 3-dimensional view of each input tensor with zero dimensions.
    Input tensors with three or more dimensions are returned as-is.

    Args:
        input (Tensor or list of Tensors)

    Returns:
        output (Tensor or tuple of Tensors)

    Example:

        >>> x = torch.tensor(0.5)
        >>> x
        tensor(0.5000)
        >>> torch.atleast_3d(x)
        tensor([[[0.5000]]])
        >>> y = torch.arange(4).view(2, 2)
        >>> y
        tensor([[0, 1],
                [2, 3]])
        >>> torch.atleast_3d(y)
        tensor([[[0],
                 [1]],
                <BLANKLINE>
                [[2],
                 [3]]])
        >>> x = torch.tensor(1).view(1, 1, 1)
        >>> x
        tensor([[[1]]])
        >>> torch.atleast_3d(x)
        tensor([[[1]]])
        >>> x = torch.tensor(0.5)
        >>> y = torch.tensor(1.0)
        >>> torch.atleast_3d((x, y))
        (tensor([[[0.5000]]]), tensor([[[1.]]]))
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(atleast_3d, tensors, *tensors)
    if len(tensors) == 1:
        tensors = tensors[0]
    return _VF.atleast_3d(tensors)  # type: ignore[attr-defined]
