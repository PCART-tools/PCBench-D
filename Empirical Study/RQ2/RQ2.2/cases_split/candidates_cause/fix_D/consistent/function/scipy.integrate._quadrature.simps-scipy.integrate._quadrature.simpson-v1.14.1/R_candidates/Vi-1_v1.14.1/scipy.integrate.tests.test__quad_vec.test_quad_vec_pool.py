@pytest.mark.fail_slow(5)
def test_quad_vec_pool():
    f = _lorenzian
    res, err = quad_vec(f, -np.inf, np.inf, norm='max', epsabs=1e-4, workers=4)
    assert_allclose(res, np.pi, rtol=0, atol=1e-4)

    with Pool(10) as pool:
        def f(x):
            return 1 / (1 + x ** 2)
        res, _ = quad_vec(f, -np.inf, np.inf, norm='max', epsabs=1e-4, workers=pool.map)
        assert_allclose(res, np.pi, rtol=0, atol=1e-4)
