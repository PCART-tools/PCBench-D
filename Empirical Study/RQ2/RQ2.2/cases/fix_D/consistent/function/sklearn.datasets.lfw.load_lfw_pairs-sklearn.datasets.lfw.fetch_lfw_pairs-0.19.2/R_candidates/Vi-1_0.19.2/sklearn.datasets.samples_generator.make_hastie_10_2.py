def make_hastie_10_2(n_samples=12000, random_state=None):
    """Generates data for binary classification used in
    Hastie et al. 2009, Example 10.2.

    The ten features are standard independent Gaussian and
    the target ``y`` is defined by::

      y[i] = 1 if np.sum(X[i] ** 2) > 9.34 else -1

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, optional (default=12000)
        The number of samples.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Returns
    -------
    X : array of shape [n_samples, 10]
        The input samples.

    y : array of shape [n_samples]
        The output values.

    References
    ----------
    .. [1] T. Hastie, R. Tibshirani and J. Friedman, "Elements of Statistical
           Learning Ed. 2", Springer, 2009.

    See also
    --------
    make_gaussian_quantiles: a generalization of this dataset approach
    """
    rs = check_random_state(random_state)

    shape = (n_samples, 10)
    X = rs.normal(size=shape).reshape(shape)
    y = ((X ** 2.0).sum(axis=1) > 9.34).astype(np.float64)
    y[y == 0.0] = -1.0

    return X, y
