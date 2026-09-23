def assert_equal_inf_nan(v1,v2,msg):
    npt.assert_(not np.isnan(v1))
    if not np.isinf(v1):
        npt.assert_almost_equal(v1, v2, decimal=DECIMAL, err_msg=msg +
                                   ' - finite')
    else:
        npt.assert_(np.isinf(v2) or np.isnan(v2),
               msg + ' - infinite, v2=%s' % str(v2))
