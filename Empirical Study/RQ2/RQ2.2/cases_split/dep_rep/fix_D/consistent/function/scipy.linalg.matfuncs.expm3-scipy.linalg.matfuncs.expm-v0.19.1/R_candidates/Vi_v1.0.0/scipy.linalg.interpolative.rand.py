def rand(*shape):
    """
    Generate standard uniform pseudorandom numbers via a very efficient lagged
    Fibonacci method.

    This routine is used for all random number generation in this package and
    can affect ID and SVD results.

    Parameters
    ----------
    shape
        Shape of output array

    """
    # For details, see :func:`backend.id_srand`, and :func:`backend.id_srando`.
    return backend.id_srand(np.prod(shape)).reshape(shape)
