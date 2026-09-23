def pseudorandom(n, p, random_state=None):
    """ Pseudorandom array of integer indexes

    >>> pseudorandom(5, [0.5, 0.5], random_state=123)
    array([1, 0, 0, 1, 1], dtype=int8)

    >>> pseudorandom(10, [0.5, 0.2, 0.2, 0.1], random_state=5)
    array([0, 2, 0, 3, 0, 1, 2, 1, 0, 0], dtype=int8)
    """
    import numpy as np
    p = list(p)
    cp = np.cumsum([0] + p)
    assert np.allclose(1, cp[-1])
    assert len(p) < 256

    if not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)

    x = random_state.random_sample(n)
    out = np.empty(n, dtype='i1')

    for i, (low, high) in enumerate(zip(cp[:-1], cp[1:])):
        out[(x >= low) & (x < high)] = i
    return out
