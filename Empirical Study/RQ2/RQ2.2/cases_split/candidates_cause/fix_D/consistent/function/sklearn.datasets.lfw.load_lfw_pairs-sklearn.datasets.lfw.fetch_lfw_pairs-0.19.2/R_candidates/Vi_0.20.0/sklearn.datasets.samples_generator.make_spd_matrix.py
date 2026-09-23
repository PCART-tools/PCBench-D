def make_spd_matrix(n_dim, random_state=None):
    """Generate a random symmetric, positive-definite matrix.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_dim : int
        The matrix dimension.

    random_state : int, RandomState instance or None (default)
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : array of shape [n_dim, n_dim]
        The random symmetric, positive-definite matrix.

    See also
    --------
    make_sparse_spd_matrix
    """
    generator = check_random_state(random_state)

    A = generator.rand(n_dim, n_dim)
    U, s, V = linalg.svd(np.dot(A.T, A))
    X = np.dot(np.dot(U, 1.0 + np.diag(generator.rand(n_dim))), V)

    return X
