def random_state(random_state_argument):
    """Decorator to generate a `numpy.random.RandomState` instance.

    .. deprecated:: 2.7

       This function is a deprecated alias for `np_random_state` and will be
       removed in version 3.0. Use np_random_state instead.
    """
    import warnings

    warnings.warn(
        (
            "`random_state` is a deprecated alias for `np_random_state`\n"
            "and will be removed in version 3.0. Use `np_random_state` instead."
        ),
        DeprecationWarning,
        stacklevel=2,
    )
    return np_random_state(random_state_argument)
