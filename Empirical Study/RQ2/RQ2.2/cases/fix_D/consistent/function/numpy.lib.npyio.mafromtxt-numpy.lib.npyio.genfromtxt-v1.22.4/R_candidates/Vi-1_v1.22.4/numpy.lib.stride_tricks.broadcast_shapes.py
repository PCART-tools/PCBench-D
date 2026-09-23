@set_module('numpy')
def broadcast_shapes(*args):
    """
    Broadcast the input shapes into a single shape.

    :ref:`Learn more about broadcasting here <basics.broadcasting>`.

    .. versionadded:: 1.20.0

    Parameters
    ----------
    `*args` : tuples of ints, or ints
        The shapes to be broadcast against each other.

    Returns
    -------
    tuple
        Broadcasted shape.

    Raises
    ------
    ValueError
        If the shapes are not compatible and cannot be broadcast according
        to NumPy's broadcasting rules.

    See Also
    --------
    broadcast
    broadcast_arrays
    broadcast_to

    Examples
    --------
    >>> np.broadcast_shapes((1, 2), (3, 1), (3, 2))
    (3, 2)

    >>> np.broadcast_shapes((6, 7), (5, 6, 1), (7,), (5, 1, 7))
    (5, 6, 7)
    """
    arrays = [np.empty(x, dtype=[]) for x in args]
    return _broadcast_shape(*arrays)
