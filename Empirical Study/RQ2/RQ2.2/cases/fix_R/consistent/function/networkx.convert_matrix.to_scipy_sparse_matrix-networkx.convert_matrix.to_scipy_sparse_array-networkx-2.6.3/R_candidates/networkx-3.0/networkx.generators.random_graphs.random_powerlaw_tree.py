@py_random_state(2)
def random_powerlaw_tree(n, gamma=3, seed=None, tries=100):
    """Returns a tree with a power law degree distribution.

    Parameters
    ----------
    n : int
        The number of nodes.
    gamma : float
        Exponent of the power law.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    tries : int
        Number of attempts to adjust the sequence to make it a tree.

    Raises
    ------
    NetworkXError
        If no valid sequence is found within the maximum number of
        attempts.

    Notes
    -----
    A trial power law degree sequence is chosen and then elements are
    swapped with new elements from a powerlaw distribution until the
    sequence makes a tree (by checking, for example, that the number of
    edges is one smaller than the number of nodes).

    """
    # This call may raise a NetworkXError if the number of tries is succeeded.
    seq = random_powerlaw_tree_sequence(n, gamma=gamma, seed=seed, tries=tries)
    G = degree_sequence_tree(seq)
    return G
