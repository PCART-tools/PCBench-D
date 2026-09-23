def random_state_data(n, random_state=None):
    """Return a list of arrays that can initialize
    ``np.random.RandomState``.

    Parameters
    ----------
    n : int
        Number of tuples to return.
    random_state : int or np.random.RandomState, optional
        If an int, is used to seed a new ``RandomState``.
    """
    import numpy as np

    if not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)

    maxuint32 = np.iinfo(np.uint32).max
    return [(random_state.rand(624) * maxuint32).astype('uint32')
            for i in range(n)]
