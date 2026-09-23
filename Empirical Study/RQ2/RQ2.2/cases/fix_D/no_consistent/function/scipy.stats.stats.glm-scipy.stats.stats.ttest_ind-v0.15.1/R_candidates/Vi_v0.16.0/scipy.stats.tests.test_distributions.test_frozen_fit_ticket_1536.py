def test_frozen_fit_ticket_1536():
    np.random.seed(5678)
    true = np.array([0.25, 0., 0.5])
    x = stats.lognorm.rvs(true[0], true[1], true[2], size=100)

    olderr = np.seterr(divide='ignore')
    try:
        params = np.array(stats.lognorm.fit(x, floc=0.))
    finally:
        np.seterr(**olderr)

    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, fscale=0.5, loc=0))
    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, f0=0.25, loc=0))
    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, f0=0.25, floc=0))
    assert_almost_equal(params, true, decimal=2)

    np.random.seed(5678)
    loc = 1
    floc = 0.9
    x = stats.norm.rvs(loc, 2., size=100)
    params = np.array(stats.norm.fit(x, floc=floc))
    expected = np.array([floc, np.sqrt(((x-floc)**2).mean())])
    assert_almost_equal(params, expected, decimal=4)
