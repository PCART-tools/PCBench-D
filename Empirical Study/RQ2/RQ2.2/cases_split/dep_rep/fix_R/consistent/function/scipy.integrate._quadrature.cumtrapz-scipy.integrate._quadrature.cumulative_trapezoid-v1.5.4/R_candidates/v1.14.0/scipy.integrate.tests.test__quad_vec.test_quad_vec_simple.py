@quadrature_params
def test_quad_vec_simple(quadrature):
    n = np.arange(10)
    def f(x):
        return x ** n
    for epsabs in [0.1, 1e-3, 1e-6]:
        if quadrature == 'trapezoid' and epsabs < 1e-4:
            # slow: skip
            continue

        kwargs = dict(epsabs=epsabs, quadrature=quadrature)

        exact = 2**(n+1)/(n + 1)

        res, err = quad_vec(f, 0, 2, norm='max', **kwargs)
        assert_allclose(res, exact, rtol=0, atol=epsabs)

        res, err = quad_vec(f, 0, 2, norm='2', **kwargs)
        assert np.linalg.norm(res - exact) < epsabs

        res, err = quad_vec(f, 0, 2, norm='max', points=(0.5, 1.0), **kwargs)
        assert_allclose(res, exact, rtol=0, atol=epsabs)

        res, err, *rest = quad_vec(f, 0, 2, norm='max',
                                   epsrel=1e-8,
                                   full_output=True,
                                   limit=10000,
                                   **kwargs)
        assert_allclose(res, exact, rtol=0, atol=epsabs)
