def check_sample_meanvar(sm,m,msg):
    if not np.isinf(m) and not np.isnan(m):
        npt.assert_almost_equal(sm, m, decimal=DECIMAL, err_msg=msg +
                                ' - finite moment')
