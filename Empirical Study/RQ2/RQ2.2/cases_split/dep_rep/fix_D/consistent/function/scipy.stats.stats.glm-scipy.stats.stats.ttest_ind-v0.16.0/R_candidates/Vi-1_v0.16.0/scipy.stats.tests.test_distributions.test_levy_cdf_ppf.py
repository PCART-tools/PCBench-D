def test_levy_cdf_ppf():
    # Test levy.cdf, including small arguments.
    x = np.array([1000, 1.0, 0.5, 0.1, 0.01, 0.001])

    # Expected values were calculated separately with mpmath.
    # E.g.
    # >>> mpmath.mp.dps = 100
    # >>> x = mpmath.mp.mpf('0.01')
    # >>> cdf = mpmath.erfc(mpmath.sqrt(1/(2*x)))
    expected = np.array([0.9747728793699604,
                         0.3173105078629141,
                         0.1572992070502851,
                         0.0015654022580025495,
                         1.523970604832105e-23,
                         1.795832784800726e-219])

    y = stats.levy.cdf(x)
    assert_allclose(y, expected, rtol=1e-10)

    # ppf(expected) should get us back to x.
    xx = stats.levy.ppf(expected)
    assert_allclose(xx, x, rtol=1e-13)
