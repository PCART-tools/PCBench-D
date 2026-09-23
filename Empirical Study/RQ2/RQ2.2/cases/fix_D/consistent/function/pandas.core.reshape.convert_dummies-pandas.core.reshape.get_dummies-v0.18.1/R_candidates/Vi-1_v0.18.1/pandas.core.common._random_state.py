def _random_state(state=None):
    """
    Helper function for processing random_state arguments.

    Parameters
    ----------
    state : int, np.random.RandomState, None.
        If receives an int, passes to np.random.RandomState() as seed.
        If receives an np.random.RandomState object, just returns object.
        If receives `None`, returns an np.random.RandomState object.
        If receives anything else, raises an informative ValueError.
        Default None.

    Returns
    -------
    np.random.RandomState
    """

    if is_integer(state):
        return np.random.RandomState(state)
    elif isinstance(state, np.random.RandomState):
        return state
    elif state is None:
        return np.random.RandomState()
    else:
        raise ValueError("random_state must be an integer, a numpy "
                         "RandomState, or None")
