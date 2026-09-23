def make_gaussian_quantiles(mean=None, cov=1., n_samples=100,
                            n_features=2, n_classes=3,
                            shuffle=True, random_state=None):
    r"""Generate isotropic Gaussian and label samples by quantile

    This classification dataset is constructed by taking a multi-dimensional
    standard normal distribution and defining classes separated by nested
    concentric multi-dimensional spheres such that roughly equal numbers of
    samples are in each class (quantiles of the :math:`\chi^2` distribution).

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    mean : array of shape [n_features], optional (default=None)
        The mean of the multi-dimensional normal distribution.
        If None then use the origin (0, 0, ...).

    cov : float, optional (default=1.)
        The covariance matrix will be this value times the unit matrix. This
        dataset only produces symmetric normal distributions.

    n_samples : int, optional (default=100)
        The total number of points equally divided among classes.

    n_features : int, optional (default=2)
        The number of features for each sample.

    n_classes : int, optional (default=3)
        The number of classes

    shuffle : boolean, optional (default=True)
        Shuffle the samples.

    random_state : int, RandomState instance or None (default)
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : array of shape [n_samples, n_features]
        The generated samples.

    y : array of shape [n_samples]
        The integer labels for quantile membership of each sample.

    Notes
    -----
    The dataset is from Zhu et al [1].

    References
    ----------
    .. [1] J. Zhu, H. Zou, S. Rosset, T. Hastie, "Multi-class AdaBoost", 2009.

    """
    if n_samples < n_classes:
        raise ValueError("n_samples must be at least n_classes")

    generator = check_random_state(random_state)

    if mean is None:
        mean = np.zeros(n_features)
    else:
        mean = np.array(mean)

    # Build multivariate normal distribution
    X = generator.multivariate_normal(mean, cov * np.identity(n_features),
                                      (n_samples,))

    # Sort by distance from origin
    idx = np.argsort(np.sum((X - mean[np.newaxis, :]) ** 2, axis=1))
    X = X[idx, :]

    # Label by quantile
    step = n_samples // n_classes

    y = np.hstack([np.repeat(np.arange(n_classes), step),
                   np.repeat(n_classes - 1, n_samples - step * n_classes)])

    if shuffle:
        X, y = util_shuffle(X, y, random_state=generator)

    return X, y
