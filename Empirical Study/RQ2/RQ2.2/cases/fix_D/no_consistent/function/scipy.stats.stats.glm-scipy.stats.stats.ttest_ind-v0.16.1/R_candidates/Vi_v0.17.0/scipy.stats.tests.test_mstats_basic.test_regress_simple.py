def test_regress_simple():
    # Regress a line with sinusoidal noise. Test for #1273.
    x = np.linspace(0, 100, 100)
    y = 0.2 * np.linspace(0, 100, 100) + 10
    y += np.sin(np.linspace(0, 20, 100))

    slope, intercept, r_value, p_value, sterr = mstats.linregress(x, y)
    assert_almost_equal(slope, 0.19644990055858422)
    assert_almost_equal(intercept, 10.211269918932341)

    # test for namedtuple attributes
    res = mstats.linregress(x, y)
    attributes = ('slope', 'intercept', 'rvalue', 'pvalue', 'stderr')
    check_named_results(res, attributes, ma=True)
