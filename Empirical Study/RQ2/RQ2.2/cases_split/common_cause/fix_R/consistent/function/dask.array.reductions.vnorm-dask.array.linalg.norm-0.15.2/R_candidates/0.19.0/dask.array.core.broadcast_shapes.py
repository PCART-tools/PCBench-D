def broadcast_shapes(*shapes):
    """
    Determines output shape from broadcasting arrays.

    Parameters
    ----------
    shapes : tuples
        The shapes of the arguments.

    Returns
    -------
    output_shape : tuple

    Raises
    ------
    ValueError
        If the input shapes cannot be successfully broadcast together.
    """
    if len(shapes) == 1:
        return shapes[0]
    out = []
    for sizes in zip_longest(*map(reversed, shapes), fillvalue=-1):
        dim = 0 if 0 in sizes else np.max(sizes)
        if any(i not in [-1, 0, 1, dim] and not np.isnan(i) for i in sizes):
            raise ValueError("operands could not be broadcast together with "
                             "shapes {0}".format(' '.join(map(str, shapes))))
        out.append(dim)
    return tuple(reversed(out))
