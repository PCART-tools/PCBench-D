def test_normalitytests():
    # numbers verified with R: dagoTest in package fBasics
    st_normal, st_skew, st_kurt = (3.92371918, 1.98078826, -0.01403734)
    pv_normal, pv_skew, pv_kurt = (0.14059673, 0.04761502, 0.98880019)
    x = np.array((-2,-1,0,1,2,3)*4)**2
    yield assert_array_almost_equal, stats.normaltest(x), (st_normal, pv_normal)
    yield assert_array_almost_equal, stats.skewtest(x), (st_skew, pv_skew)
    yield assert_array_almost_equal, stats.kurtosistest(x), (st_kurt, pv_kurt)

    # Test axis=None (equal to axis=0 for 1-D input)
    yield (assert_array_almost_equal, stats.normaltest(x, axis=None),
           (st_normal, pv_normal))
    yield (assert_array_almost_equal, stats.skewtest(x, axis=None),
           (st_skew, pv_skew))
    yield (assert_array_almost_equal, stats.kurtosistest(x, axis=None),
           (st_kurt, pv_kurt))
