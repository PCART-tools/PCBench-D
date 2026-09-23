def test_regression_tukey_lambda():
    # Make sure that Tukey-Lambda distribution correctly handles
    # non-positive lambdas.
    x = np.linspace(-5.0, 5.0, 101)

    olderr = np.seterr(divide='ignore')
    try:
        for lam in [0.0, -1.0, -2.0, np.array([[-1.0], [0.0], [-2.0]])]:
            p = stats.tukeylambda.pdf(x, lam)
            assert_((p != 0.0).all())
            assert_(~np.isnan(p).all())

        lam = np.array([[-1.0], [0.0], [2.0]])
        p = stats.tukeylambda.pdf(x, lam)
    finally:
        np.seterr(**olderr)

    assert_(~np.isnan(p).all())
    assert_((p[0] != 0.0).all())
    assert_((p[1] != 0.0).all())
    assert_((p[2] != 0.0).any())
    assert_((p[2] == 0.0).any())
