def test_kde_2d():
    #some basic tests comparing to normal distribution
    np.random.seed(8765678)
    n_basesample = 500

    mean = np.array([1.0, 3.0])
    covariance = np.array([[1.0, 2.0], [2.0, 6.0]])

    # Need transpose (shape (2, 500)) for kde
    xn = np.random.multivariate_normal(mean, covariance, size=n_basesample).T

    # get kde for original sample
    gkde = stats.gaussian_kde(xn)

    # evaluate the density function for the kde for some points
    x, y = np.mgrid[-7:7:500j, -7:7:500j]
    grid_coords = np.vstack([x.ravel(), y.ravel()])
    kdepdf = gkde.evaluate(grid_coords)
    kdepdf = kdepdf.reshape(500, 500)

    normpdf = stats.multivariate_normal.pdf(np.dstack([x, y]), mean=mean, cov=covariance)
    intervall = y.ravel()[1] - y.ravel()[0]

    assert_(np.sum((kdepdf - normpdf)**2) * (intervall**2) < 0.01)

    small = -1e100
    large = 1e100
    prob1 = gkde.integrate_box([small, mean[1]], [large, large])
    prob2 = gkde.integrate_box([small, small], [large, mean[1]])

    assert_almost_equal(prob1, 0.5, decimal=1)
    assert_almost_equal(prob2, 0.5, decimal=1)
    assert_almost_equal(gkde.integrate_kde(gkde),
                        (kdepdf**2).sum()*(intervall**2), decimal=2)
    assert_almost_equal(gkde.integrate_gaussian(mean, covariance),
                        (kdepdf*normpdf).sum()*(intervall**2), decimal=2)
