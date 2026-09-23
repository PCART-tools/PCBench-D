def cwt_matrix(n_rows, n_columns, seed=None):
    r""""
    Generate a matrix S for the Clarkson-Woodruff sketch.

    Given the desired size of matrix, the method returns a matrix S of size
    (n_rows, n_columns) where each column has all the entries set to 0 less one
    position which has been randomly set to +1 or -1 with equal probability.

    Parameters
    ----------
    n_rows: int
        Number of rows of S
    n_columns: int
        Number of columns of S
    seed : None or int or `numpy.random.RandomState` instance, optional
        This parameter defines the ``RandomState`` object to use for drawing
        random variates.
        If None (or ``np.random``), the global ``np.random`` state is used.
        If integer, it is used to seed the local ``RandomState`` instance.
        Default is None.

    Returns
    -------
    S : (n_rows, n_columns) array_like

    Notes
    -----
    Given a matrix A, with probability at least 9/10,
    .. math:: ||SA|| == (1 \pm \epsilon)||A||
    Where epsilon is related to the size of S
    """
    S = np.zeros((n_rows, n_columns))
    nz_positions = np.random.randint(0, n_rows, n_columns)
    rng = check_random_state(seed)
    values = rng.choice([1, -1], n_columns)
    for i in range(n_columns):
        S[nz_positions[i]][i] = values[i]

    return S
