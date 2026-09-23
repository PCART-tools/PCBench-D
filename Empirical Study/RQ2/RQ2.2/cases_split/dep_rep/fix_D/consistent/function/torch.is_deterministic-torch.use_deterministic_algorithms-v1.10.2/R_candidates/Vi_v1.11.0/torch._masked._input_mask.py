def _input_mask(input: Tensor, *args, **kwargs) -> Tensor:
    """Return canonical input mask.
    Canonical input mask is a boolean tensor with the same shape as
    input and with (broadcasted) content of mask, if specified.
    """
    mask = kwargs.get('mask')
    if mask is None:
        inmask = input.new_ones(input.shape, dtype=torch.bool)
    elif mask.ndim < input.ndim:
        inmask = torch.broadcast_to(mask.clone(), input.shape).to(dtype=torch.bool)
    elif mask.ndim > input.ndim:
        raise IndexError("_input_mask expected broadcastable mask (got mask dimensionality higher than of the input)")
    elif mask.shape != input.shape:
        inmask = torch.broadcast_to(mask.clone(), input.shape).to(dtype=torch.bool)
    else:
        inmask = mask.to(dtype=torch.bool)
    return inmask
