def test_ttest_ind_with_uneq_var():
    # check vs. R
    a = (1, 2, 3)
    b = (1.1, 2.9, 4.2)
    pr = 0.53619490753126731
    tr = -0.68649512735572582
    t, p = stats.ttest_ind(a, b, equal_var=False)
    assert_array_almost_equal([t,p], [tr, pr])
    # test from desc stats API
    assert_array_almost_equal(stats.ttest_ind_from_stats(*_desc_stats(a, b),
                                                         equal_var=False),
                              [t, p])

    a = (1, 2, 3, 4)
    pr = 0.84354139131608286
    tr = -0.2108663315950719
    t, p = stats.ttest_ind(a, b, equal_var=False)
    assert_array_almost_equal([t,p], [tr, pr])
    assert_array_almost_equal(stats.ttest_ind_from_stats(*_desc_stats(a, b),
                                                         equal_var=False),
                              [t, p])

    # regression test
    tr = 1.0912746897927283
    tr_uneq_n = 0.66745638708050492
    pr = 0.27647831993021388
    pr_uneq_n = 0.50873585065616544
    tpr = ([tr,-tr],[pr,pr])

    rvs3 = np.linspace(1,100, 25)
    rvs2 = np.linspace(1,100,100)
    rvs1 = np.linspace(5,105,100)
    rvs1_2D = np.array([rvs1, rvs2])
    rvs2_2D = np.array([rvs2, rvs1])

    t,p = stats.ttest_ind(rvs1, rvs2, axis=0, equal_var=False)
    assert_array_almost_equal([t,p],(tr,pr))
    assert_array_almost_equal(stats.ttest_ind_from_stats(*_desc_stats(rvs1,
                                                                      rvs2),
                                                         equal_var=False),
                              (t, p))

    t,p = stats.ttest_ind(rvs1, rvs3, axis=0, equal_var=False)
    assert_array_almost_equal([t,p], (tr_uneq_n, pr_uneq_n))
    assert_array_almost_equal(stats.ttest_ind_from_stats(*_desc_stats(rvs1,
                                                                      rvs3),
                                                         equal_var=False),
                              (t, p))

    t,p = stats.ttest_ind(rvs1_2D.T, rvs2_2D.T, axis=0, equal_var=False)
    assert_array_almost_equal([t,p],tpr)
    args = _desc_stats(rvs1_2D.T, rvs2_2D.T)
    assert_array_almost_equal(stats.ttest_ind_from_stats(*args,
                                                         equal_var=False),
                              (t, p))

    t,p = stats.ttest_ind(rvs1_2D, rvs2_2D, axis=1, equal_var=False)
    assert_array_almost_equal([t,p],tpr)
    args = _desc_stats(rvs1_2D, rvs2_2D, axis=1)
    assert_array_almost_equal(stats.ttest_ind_from_stats(*args,
                                                         equal_var=False),
                              (t, p))

    # test for namedtuple attribute results
    attributes = ('statistic', 'pvalue')
    res = stats.ttest_ind(rvs1, rvs2, axis=0, equal_var=False)
    check_named_results(res, attributes)

    # test on 3 dimensions
    rvs1_3D = np.dstack([rvs1_2D,rvs1_2D,rvs1_2D])
    rvs2_3D = np.dstack([rvs2_2D,rvs2_2D,rvs2_2D])
    t,p = stats.ttest_ind(rvs1_3D, rvs2_3D, axis=1, equal_var=False)
    assert_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (2, 3))
    args = _desc_stats(rvs1_3D, rvs2_3D, axis=1)
    t, p = stats.ttest_ind_from_stats(*args, equal_var=False)
    assert_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (2, 3))

    t,p = stats.ttest_ind(np.rollaxis(rvs1_3D,2), np.rollaxis(rvs2_3D,2),
                                   axis=2, equal_var=False)
    assert_array_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (3, 2))
    args = _desc_stats(np.rollaxis(rvs1_3D, 2),
                       np.rollaxis(rvs2_3D, 2), axis=2)
    t, p = stats.ttest_ind_from_stats(*args, equal_var=False)
    assert_array_almost_equal(np.abs(t), np.abs(tr))
    assert_array_almost_equal(np.abs(p), pr)
    assert_equal(t.shape, (3, 2))

    # test zero division problem
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        t, p = stats.ttest_ind([0, 0, 0], [1, 1, 1], equal_var=False)
        assert_equal((np.abs(t), p), (np.inf, 0))
        assert_equal(stats.ttest_ind([0, 0, 0], [0, 0, 0], equal_var=False),
                     (np.nan, np.nan))

    olderr = np.seterr(all='ignore')
    try:
        # check that nan in input array result in nan output
        anan = np.array([[1, np.nan], [-1, 1]])
        assert_equal(stats.ttest_ind(anan, np.zeros((2, 2)), equal_var=False),
                     ([0, np.nan], [1, np.nan]))
    finally:
        np.seterr(**olderr)
