def check_sample_meanvar(sm,m,msg):
    if not np.isinf(m):
        npt.assert_almost_equal(sm, m, decimal=DECIMAL_meanvar, err_msg=msg +
                                ' - finite moment')
    else:
        npt.assert_(sm > 10000, msg='infinite moment, sm = ' + str(sm))
