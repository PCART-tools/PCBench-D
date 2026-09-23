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
    for sizes in zip_longest(*map(reversed, shapes), fillvalue=1):
        dim = max(sizes)
        if any(i != 1 and i != dim and not np.isnan(i) for i in sizes):
            raise ValueError("operands could not be broadcast together with "
                             "shapes {0}".format(' '.join(map(str, shapes))))
        out.append(dim)
    return tuple(reversed(out))
