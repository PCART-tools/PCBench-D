def make_s_curve(n_samples=100, noise=0.0, random_state=None):
    """Generate an S curve dataset.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, optional (default=100)
        The number of sample points on the S curve.

    noise : float, optional (default=0.0)
        The standard deviation of the gaussian noise.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Returns
    -------
    X : array of shape [n_samples, 3]
        The points.

    t : array of shape [n_samples]
        The univariate position of the sample according to the main dimension
        of the points in the manifold.
    """
    generator = check_random_state(random_state)

    t = 3 * np.pi * (generator.rand(1, n_samples) - 0.5)
    x = np.sin(t)
    y = 2.0 * generator.rand(1, n_samples)
    z = np.sign(t) * (np.cos(t) - 1)

    X = np.concatenate((x, y, z))
    X += noise * generator.randn(3, n_samples)
    X = X.T
    t = np.squeeze(t)

    return X, t
