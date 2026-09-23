def atleast_1d(*tensors):
    r"""
    Returns a 1-dimensional view of each input tensor with zero dimensions.
    Input tensors with one or more dimensions are returned as-is.

    Args:
        input (Tensor or list of Tensors)

    Returns:
        output (Tensor or tuple of Tensors)

    Example::

        >>> x = torch.arange(2)
        >>> x
        tensor([0, 1])
        >>> torch.atleast_1d(x)
        tensor([0, 1])
        >>> x = torch.tensor(1.)
        >>> x
        tensor(1.)
        >>> torch.atleast_1d(x)
        tensor([1.])
        >>> x = torch.tensor(0.5)
        >>> y = torch.tensor(1.)
        >>> torch.atleast_1d((x, y))
        (tensor([0.5000]), tensor([1.]))
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(atleast_1d, tensors, *tensors)
    if len(tensors) == 1:
        tensors = tensors[0]
    return _VF.atleast_1d(tensors)  # type: ignore[attr-defined]
