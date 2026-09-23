def _multi_dot(arrays, order, i, j, precision):
    """Actually do the multiplication with the given order."""
    if i == j:
        return arrays[i]
    else:
        return jnp.dot(_multi_dot(arrays, order, i, order[i, j], precision),
                      _multi_dot(arrays, order, order[i, j] + 1, j, precision),
                      precision=precision)
