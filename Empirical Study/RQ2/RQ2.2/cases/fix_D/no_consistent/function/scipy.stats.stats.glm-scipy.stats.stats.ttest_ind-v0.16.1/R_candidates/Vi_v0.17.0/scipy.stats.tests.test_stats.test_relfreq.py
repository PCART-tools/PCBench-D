def test_relfreq():
    a = np.array([1, 4, 2, 1, 3, 1])
    relfreqs, lowlim, binsize, extrapoints = stats.relfreq(a, numbins=4)
    assert_array_almost_equal(relfreqs,
                              array([0.5, 0.16666667, 0.16666667, 0.16666667]))

    # test for namedtuple attribute results
    attributes = ('frequency', 'lowerlimit', 'binsize', 'extrapoints')
    res = stats.relfreq(a, numbins=4)
    check_named_results(res, attributes)

    # check array_like input is accepted
    relfreqs2, lowlim, binsize, extrapoints = stats.relfreq([1, 4, 2, 1, 3, 1],
                                                            numbins=4)
    assert_array_almost_equal(relfreqs, relfreqs2)
