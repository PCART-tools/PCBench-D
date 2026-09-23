def different_seeds(n, random_state=None):
    """ A list of different 32 bit integer seeds

    Parameters
    ----------
    n: int
        Number of distinct seeds to return
    random_state: int or np.random.RandomState
        If int create a new RandomState with this as the seed
    Otherwise draw from the passed RandomState
    """
    import numpy as np

    if not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)

    big_n = np.iinfo(np.int32).max

    seeds = set(random_state.randint(big_n, size=n))
    while len(seeds) < n:
        seeds.add(random_state.randint(big_n))

    # Sorting makes it easier to know what seeds are for what chunk
    return sorted(seeds)
