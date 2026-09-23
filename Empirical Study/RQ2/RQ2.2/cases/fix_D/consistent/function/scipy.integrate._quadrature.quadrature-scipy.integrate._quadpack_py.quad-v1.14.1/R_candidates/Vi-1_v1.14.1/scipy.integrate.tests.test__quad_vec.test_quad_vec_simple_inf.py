@quadrature_params
def test_quad_vec_simple_inf(quadrature):
    def f(x):
        return 1 / (1 + np.float64(x) ** 2)

    for epsabs in [0.1, 1e-3, 1e-6]:
        if quadrature == 'trapezoid' and epsabs < 1e-4:
            # slow: skip
            continue

        kwargs = dict(norm='max', epsabs=epsabs, quadrature=quadrature)

        res, err = quad_vec(f, 0, np.inf, **kwargs)
        assert_allclose(res, np.pi/2, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, 0, -np.inf, **kwargs)
        assert_allclose(res, -np.pi/2, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, -np.inf, 0, **kwargs)
        assert_allclose(res, np.pi/2, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, np.inf, 0, **kwargs)
        assert_allclose(res, -np.pi/2, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, -np.inf, np.inf, **kwargs)
        assert_allclose(res, np.pi, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, np.inf, -np.inf, **kwargs)
        assert_allclose(res, -np.pi, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, np.inf, np.inf, **kwargs)
        assert_allclose(res, 0, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, -np.inf, -np.inf, **kwargs)
        assert_allclose(res, 0, rtol=0, atol=max(epsabs, err))

        res, err = quad_vec(f, 0, np.inf, points=(1.0, 2.0), **kwargs)
        assert_allclose(res, np.pi/2, rtol=0, atol=max(epsabs, err))

    def f(x):
        return np.sin(x + 2) / (1 + x ** 2)
    exact = np.pi / np.e * np.sin(2)
    epsabs = 1e-5

    res, err, info = quad_vec(f, -np.inf, np.inf, limit=1000, norm='max', epsabs=epsabs,
                              quadrature=quadrature, full_output=True)
    assert info.status == 1
    assert_allclose(res, exact, rtol=0, atol=max(epsabs, 1.5 * err))
