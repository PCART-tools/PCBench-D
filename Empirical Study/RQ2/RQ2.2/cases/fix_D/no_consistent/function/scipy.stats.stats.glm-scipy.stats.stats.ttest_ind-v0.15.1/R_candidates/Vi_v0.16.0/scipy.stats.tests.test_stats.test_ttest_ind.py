def test_ttest_ind():
    # regression test
    tr = 1.0912746897927283
    pr = 0.27647818616351882
    tpr = ([tr,-tr],[pr,pr])

    rvs2 = np.linspace(1,100,100)
    rvs1 = np.linspace(5,105,100)
    rvs1_2D = np.array([rvs1, rvs2])
    rvs2_2D = np.array([rvs2, rvs1])

    t,p = stats.ttest_ind(rvs1, rvs2, axis=0)
    assert_array_almost_equal([t,p],(tr,pr))
    # test from_stats API
    assert_array_almost_equal(stats.ttest_ind_from_stats(*_desc_stats(rvs1,
                                                                      rvs2)),
                              [t, p])
    t,p = stats.ttest_ind(rvs1_2D.T, rvs2_2D.T, axis=0)
    assert_array_almost_equal([t,p],tpr)
    args = _desc_stats(rvs1_2D.T, rvs2_2D.T)
    assert_array_almost_equal(stats.ttest_ind_from_stats(*args),
                              [t, p])
    t,p = stats.ttest_ind(rvs1_2D, rvs2_2D, axis=1)
    assert_array_almost_equal([t,p],tpr)
    args = _desc_stats(rvs1_2D, rvs2_2D, axis=1)
    assert_array_almost_equal(stats.ttest_ind_from_stats(*args),
                              [t, p])

    # test scalars
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        t, p = stats.ttest_ind(4., 3.)
    assert_(np.isnan(t))
    assert_(np.isnan(p))

    # test on 3 dimensions
    rvs1_3D = np.dstack([rvs1_2D,rvs1_2D,rvs1_2D])
    rvs2_3D = np.dstack([rvs2_2D,rvs2_2D,rvs2_2D])
    t,p = stats.ttest_ind(rvs1_3D, rvs2_3D, axis=1)
    assert_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (2, 3))

    t,p = stats.ttest_ind(np.rollaxis(rvs1_3D,2), np.rollaxis(rvs2_3D,2), axis=2)
    assert_array_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (3, 2))

    olderr = np.seterr(all='ignore')
    try:
        # test zero division problem
        t,p = stats.ttest_ind([0,0,0],[1,1,1])
        assert_equal((np.abs(t),p), (np.inf, 0))
        assert_equal(stats.ttest_ind([0,0,0], [0,0,0]), (np.nan, np.nan))

        # check that nan in input array result in nan output
        anan = np.array([[1,np.nan],[-1,1]])
        assert_equal(stats.ttest_ind(anan, np.zeros((2,2))),([0, np.nan], [1,np.nan]))
    finally:
        np.seterr(**olderr)
