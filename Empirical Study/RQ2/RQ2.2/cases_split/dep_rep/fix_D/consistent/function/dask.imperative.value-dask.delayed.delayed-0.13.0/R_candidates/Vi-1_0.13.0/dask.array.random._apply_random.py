def _apply_random(func, state_data, size, args, kwargs):
    """Apply RandomState method with seed"""
    state = np.random.RandomState(state_data)
    func = getattr(state, func)
    return func(*args, size=size, **kwargs)
