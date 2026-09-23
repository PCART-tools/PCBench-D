def get_backend():
    """
    Return the name of the current backend.

    See Also
    --------
    matplotlib.use
    """
    return rcParams['backend']
