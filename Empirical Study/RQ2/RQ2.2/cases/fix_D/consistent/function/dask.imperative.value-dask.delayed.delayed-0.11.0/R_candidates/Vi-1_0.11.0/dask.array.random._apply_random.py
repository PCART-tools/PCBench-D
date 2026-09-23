def _apply_random(func, seed, size, args, kwargs):
    """ Apply RandomState method with seed

    >>> _apply_random('normal', 123, 3, (10, 1.0), {})
    array([  8.9143694 ,  10.99734545,  10.2829785 ])
    """
    state = np.random.RandomState(seed)
    func = getattr(state, func)
    return func(*args, size=size, **kwargs)
