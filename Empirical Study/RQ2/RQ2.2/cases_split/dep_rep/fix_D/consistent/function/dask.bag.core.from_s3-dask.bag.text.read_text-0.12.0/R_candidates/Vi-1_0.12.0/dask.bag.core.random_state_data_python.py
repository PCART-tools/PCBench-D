def random_state_data_python(n, random_state=None):
    """Return a list of tuples that can initialize
    ``random.Random``.

    Parameters
    ----------
    n : int
        Number of tuples to return.
    random_state : int or ``random.Random``, optional
        If an int, is used to seed a new ``random.Random``.
    """
    if not isinstance(random_state, Random):
        random_state = Random(random_state)

    maxuint32 = 1 << 32
    return [tuple(random_state.randint(0, maxuint32) for i in range(624))
            for i in range(n)]
