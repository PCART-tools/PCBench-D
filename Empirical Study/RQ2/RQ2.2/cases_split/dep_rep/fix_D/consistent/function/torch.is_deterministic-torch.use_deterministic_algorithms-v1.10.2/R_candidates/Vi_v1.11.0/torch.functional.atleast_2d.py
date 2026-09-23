def atleast_2d(*tensors):
    r"""
    Returns a 2-dimensional view of each input tensor with zero dimensions.
    Input tensors with two or more dimensions are returned as-is.

    Args:
        input (Tensor or list of Tensors)

    Returns:
        output (Tensor or tuple of Tensors)

    Example::

        >>> x = torch.tensor(1.)
        >>> x
        tensor(1.)
        >>> torch.atleast_2d(x)
        tensor([[1.]])
        >>> x = torch.randn(2,2)
        >>> x
        tensor([[2.2086, 2.5165],
                [0.1757, 0.5194]])
        >>> torch.atleast_2d(x)
        tensor([[2.2086, 2.5165],
                [0.1757, 0.5194]])
        >>> x = torch.tensor(0.5)
        >>> y = torch.tensor(1.)
        >>> torch.atleast_2d((x,y))
        (tensor([[0.5000]]), tensor([[1.]]))
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(atleast_2d, tensors, *tensors)
    if len(tensors) == 1:
        tensors = tensors[0]
    return _VF.atleast_2d(tensors)  # type: ignore[attr-defined]
