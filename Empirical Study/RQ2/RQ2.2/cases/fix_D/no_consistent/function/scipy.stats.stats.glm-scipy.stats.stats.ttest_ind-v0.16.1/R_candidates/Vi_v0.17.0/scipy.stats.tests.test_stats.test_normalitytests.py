def test_normalitytests():
    yield (assert_raises, ValueError, stats.skewtest, 4.)
    yield (assert_raises, ValueError, stats.kurtosistest, 4.)
    yield (assert_raises, ValueError, stats.normaltest, 4.)

    # numbers verified with R: dagoTest in package fBasics
    st_normal, st_skew, st_kurt = (3.92371918, 1.98078826, -0.01403734)
    pv_normal, pv_skew, pv_kurt = (0.14059673, 0.04761502, 0.98880019)
    x = np.array((-2,-1,0,1,2,3)*4)**2
    attributes = ('statistic', 'pvalue')

    yield assert_array_almost_equal, stats.normaltest(x), (st_normal, pv_normal)
    check_named_results(stats.normaltest(x), attributes)
    yield assert_array_almost_equal, stats.skewtest(x), (st_skew, pv_skew)
    check_named_results(stats.skewtest(x), attributes)
    yield assert_array_almost_equal, stats.kurtosistest(x), (st_kurt, pv_kurt)
    check_named_results(stats.kurtosistest(x), attributes)

    # Test axis=None (equal to axis=0 for 1-D input)
    yield (assert_array_almost_equal, stats.normaltest(x, axis=None),
           (st_normal, pv_normal))
    yield (assert_array_almost_equal, stats.skewtest(x, axis=None),
           (st_skew, pv_skew))
    yield (assert_array_almost_equal, stats.kurtosistest(x, axis=None),
           (st_kurt, pv_kurt))

    x = np.arange(10.)
    x[9] = np.nan
    assert_array_equal(stats.skewtest(x), (np.nan, np.nan))

    expected = (1.0184643553962129, 0.30845733195153502)
    assert_array_almost_equal(stats.skewtest(x, nan_policy='omit'), expected)

    assert_raises(ValueError, stats.skewtest, x, nan_policy='raise')
    assert_raises(ValueError, stats.skewtest, x, nan_policy='foobar')

    x = np.arange(30.)
    x[29] = np.nan
    assert_array_equal(stats.kurtosistest(x), (np.nan, np.nan))

    expected = (-2.2683547379505273, 0.023307594135872967)
    assert_array_almost_equal(stats.kurtosistest(x, nan_policy='omit'),
                              expected)

    assert_raises(ValueError, stats.kurtosistest, x, nan_policy='raise')
    assert_raises(ValueError, stats.kurtosistest, x, nan_policy='foobar')

    assert_array_equal(stats.normaltest(x), (np.nan, np.nan))

    expected = (6.2260409514287449, 0.04446644248650191)
    assert_array_almost_equal(stats.normaltest(x, nan_policy='omit'), expected)

    assert_raises(ValueError, stats.normaltest, x, nan_policy='raise')
    assert_raises(ValueError, stats.normaltest, x, nan_policy='foobar')
