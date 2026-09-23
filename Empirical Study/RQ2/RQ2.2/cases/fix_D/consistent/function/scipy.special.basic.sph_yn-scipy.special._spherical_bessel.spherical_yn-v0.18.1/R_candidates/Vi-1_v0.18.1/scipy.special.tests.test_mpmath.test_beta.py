@check_version(mpmath, '0.15')
def test_beta():
    np.random.seed(1234)

    b = np.r_[np.logspace(-200, 200, 4),
              np.logspace(-10, 10, 4),
              np.logspace(-1, 1, 4),
              np.arange(-10, 11, 1),
              np.arange(-10, 11, 1) + 0.5,
              -1, -2.3, -3, -100.3, -10003.4]
    a = b

    ab = np.array(np.broadcast_arrays(a[:,None], b[None,:])).reshape(2, -1).T

    old_dps, old_prec = mpmath.mp.dps, mpmath.mp.prec
    try:
        mpmath.mp.dps = 400

        assert_func_equal(sc.beta,
                          lambda a, b: float(mpmath.beta(a, b)),
                          ab,
                          vectorized=False,
                          rtol=1e-10,
                          ignore_inf_sign=True)

        assert_func_equal(
            sc.betaln,
            lambda a, b: float(mpmath.log(abs(mpmath.beta(a, b)))),
            ab,
            vectorized=False,
            rtol=1e-10)
    finally:
        mpmath.mp.dps, mpmath.mp.prec = old_dps, old_prec
