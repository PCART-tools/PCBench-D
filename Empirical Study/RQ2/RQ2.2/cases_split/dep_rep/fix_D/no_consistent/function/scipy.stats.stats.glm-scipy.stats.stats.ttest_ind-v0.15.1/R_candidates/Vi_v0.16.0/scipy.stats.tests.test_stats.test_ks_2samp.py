def test_ks_2samp():
    # exact small sample solution
    data1 = np.array([1.0,2.0])
    data2 = np.array([1.0,2.0,3.0])
    assert_almost_equal(np.array(stats.ks_2samp(data1+0.01,data2)),
                np.array((0.33333333333333337, 0.99062316386915694)))
    assert_almost_equal(np.array(stats.ks_2samp(data1-0.01,data2)),
                np.array((0.66666666666666674, 0.42490954988801982)))
    # these can also be verified graphically
    assert_almost_equal(
        np.array(stats.ks_2samp(np.linspace(1,100,100),
                              np.linspace(1,100,100)+2+0.1)),
        np.array((0.030000000000000027, 0.99999999996005062)))
    assert_almost_equal(
        np.array(stats.ks_2samp(np.linspace(1,100,100),
                              np.linspace(1,100,100)+2-0.1)),
        np.array((0.020000000000000018, 0.99999999999999933)))
    # these are just regression tests
    assert_almost_equal(
        np.array(stats.ks_2samp(np.linspace(1,100,100),
                              np.linspace(1,100,110)+20.1)),
        np.array((0.21090909090909091, 0.015880386730710221)))
    assert_almost_equal(
        np.array(stats.ks_2samp(np.linspace(1,100,100),
                              np.linspace(1,100,110)+20-0.1)),
        np.array((0.20818181818181825, 0.017981441789762638)))

    # test for namedtuple attribute results
    attributes = ('statistic', 'pvalue')
    res = stats.ks_2samp(data1 - 0.01, data2)
    check_named_results(res, attributes)
