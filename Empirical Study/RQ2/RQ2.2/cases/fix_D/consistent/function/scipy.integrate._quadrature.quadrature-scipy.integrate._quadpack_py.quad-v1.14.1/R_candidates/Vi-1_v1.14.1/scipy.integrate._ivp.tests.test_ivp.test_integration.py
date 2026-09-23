def test_integration():
    rtol = 1e-3
    atol = 1e-6
    y0 = [1/3, 2/9]

    for vectorized, method, t_span, jac in product(
            [False, True],
            ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA'],
            [[5, 9], [5, 1]],
            [None, jac_rational, jac_rational_sparse]):

        if vectorized:
            fun = fun_rational_vectorized
        else:
            fun = fun_rational

        with suppress_warnings() as sup:
            sup.filter(UserWarning,
                       "The following arguments have no effect for a chosen "
                       "solver: `jac`")
            res = solve_ivp(fun, t_span, y0, rtol=rtol,
                            atol=atol, method=method, dense_output=True,
                            jac=jac, vectorized=vectorized)
        assert_equal(res.t[0], t_span[0])
        assert_(res.t_events is None)
        assert_(res.y_events is None)
        assert_(res.success)
        assert_equal(res.status, 0)

        if method == 'DOP853':
            # DOP853 spends more functions evaluation because it doesn't
            # have enough time to develop big enough step size.
            assert_(res.nfev < 50)
        else:
            assert_(res.nfev < 40)

        if method in ['RK23', 'RK45', 'DOP853', 'LSODA']:
            assert_equal(res.njev, 0)
            assert_equal(res.nlu, 0)
        else:
            assert_(0 < res.njev < 3)
            assert_(0 < res.nlu < 10)

        y_true = sol_rational(res.t)
        e = compute_error(res.y, y_true, rtol, atol)
        assert_(np.all(e < 5))

        tc = np.linspace(*t_span)
        yc_true = sol_rational(tc)
        yc = res.sol(tc)

        e = compute_error(yc, yc_true, rtol, atol)
        assert_(np.all(e < 5))

        tc = (t_span[0] + t_span[-1]) / 2
        yc_true = sol_rational(tc)
        yc = res.sol(tc)

        e = compute_error(yc, yc_true, rtol, atol)
        assert_(np.all(e < 5))

        assert_allclose(res.sol(res.t), res.y, rtol=1e-15, atol=1e-15)
