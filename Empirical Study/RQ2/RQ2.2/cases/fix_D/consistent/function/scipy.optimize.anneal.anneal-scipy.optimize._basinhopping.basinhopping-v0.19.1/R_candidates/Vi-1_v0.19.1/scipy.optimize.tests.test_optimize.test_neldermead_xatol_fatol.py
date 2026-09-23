def test_neldermead_xatol_fatol():
    # gh4484
    # test we can call with fatol, xatol specified
    func = lambda x: x[0]**2 + x[1]**2

    optimize._minimize._minimize_neldermead(func, [1, 1], maxiter=2,
                                            xatol=1e-3, fatol=1e-3)
    assert_warns(DeprecationWarning,
                 optimize._minimize._minimize_neldermead,
                 func, [1, 1], xtol=1e-3, ftol=1e-3, maxiter=2)
