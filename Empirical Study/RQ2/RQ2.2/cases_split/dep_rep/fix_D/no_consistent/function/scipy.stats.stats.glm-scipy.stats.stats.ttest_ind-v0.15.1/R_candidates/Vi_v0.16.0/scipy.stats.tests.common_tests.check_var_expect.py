def check_var_expect(distfn, arg, m, v, msg):
    if np.isfinite(v):
        m2 = distfn.expect(lambda x: x*x, arg)
        npt.assert_almost_equal(m2, v + m*m, decimal=5, err_msg=msg +
                            ' - 2st moment (expect)')
