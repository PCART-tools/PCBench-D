def preserve_random_state(func):
    """Decorator to preserve the numpy.random state during a function.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.

    Parameters
    ----------
    func : function
        function around which to preserve the random state.

    Returns
    -------
    wrapper : function
        Function which wraps the input function by saving the state before
        calling the function and restoring the function afterward.

    Examples
    --------
    Decorate functions like this::

        @preserve_random_state
        def do_random_stuff(x, y):
            return x + y * numpy.random.random()

    Notes
    -----
    If numpy.random is not importable, the state is not saved or restored.
    """
    import warnings

    msg = "preserve_random_state is deprecated and will be removed in 3.0."
    warnings.warn(msg, DeprecationWarning)

    try:
        import numpy as np

        @contextmanager
        def save_random_state():
            state = np.random.get_state()
            try:
                yield
            finally:
                np.random.set_state(state)

        def wrapper(*args, **kwargs):
            with save_random_state():
                np.random.seed(1234567890)
                return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper
    except ImportError:
        return func
