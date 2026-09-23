def check_sample_var(sm,m,msg):
    npt.assert_almost_equal(sm, m, decimal=DECIMAL_meanvar, err_msg=msg + 'var')
