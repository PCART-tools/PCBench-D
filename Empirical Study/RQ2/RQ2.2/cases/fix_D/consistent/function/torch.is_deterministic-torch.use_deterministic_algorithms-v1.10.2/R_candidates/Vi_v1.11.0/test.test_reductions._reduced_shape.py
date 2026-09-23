def _reduced_shape(shape, dim=None, keepdim=False):
    """Computes the expected reduced shape given dim and keepdim

    Args:
        shape: The shape to reduce
        dim : The dimensions to reduce
        keepdim: If true, reduced dimensions have size 1 in the reduced shape,
            otherwise they are removed from the reduced shape.

    Returns:
        The reduced shape
    """
    if dim is None:
        return [1] * len(shape) if keepdim else []

    # Wrap negative dims
    dim = dim if isinstance(dim, Sequence) else [dim]
    dim = set(i if i >= 0 else len(shape) + i for i in dim)

    result = []
    for i, size in enumerate(shape):
        if i not in dim:
            result.append(size)
        elif keepdim:
            result.append(1)

    return result
