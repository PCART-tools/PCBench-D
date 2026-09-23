def apply_masked_normalization_along_dim(op, input, *args, **kwargs):
    """Applies normalization op along given dimension to strided x
    elements that are valid according to mask tensor.
    """
    mask = kwargs.pop('mask', None)
    dim_pos = kwargs.pop('dim_position', 0)
    if input.ndim == 0:  # scalar input
        return op(input, *args, **kwargs)
    dtype = kwargs.get('dtype', input.dtype)
    dim = args[dim_pos]
    args0 = args[:dim_pos] + (0,) + args[dim_pos + 1:]
    output = torch.zeros_like(input, dtype=dtype)
    inpmask = torch._masked._input_mask(input, mask=mask)
    dim_ = dim % input.ndim
    left_ranges = tuple(map(range, input.shape[:dim_]))
    right_ranges = tuple(map(range, input.shape[dim_ + 1:]))
    for s in itertools.product(*(left_ranges + ((slice(None),),) + right_ranges)):
        indices = inpmask[s].argwhere()
        output[s][indices] = op(input[s][indices], *args0, **kwargs)
    return output
