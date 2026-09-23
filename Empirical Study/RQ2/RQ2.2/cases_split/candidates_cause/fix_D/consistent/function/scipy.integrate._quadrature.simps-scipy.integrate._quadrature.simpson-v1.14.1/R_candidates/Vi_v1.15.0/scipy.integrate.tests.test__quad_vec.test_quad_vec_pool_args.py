@pytest.mark.fail_slow(10)
@pytest.mark.parametrize('extra_args', [2, (2,)])
@pytest.mark.parametrize('workers', [1, 10])
def test_quad_vec_pool_args(extra_args, workers):
    f = _func_with_args
    exact = np.array([0, 4/3, 8/3])

    res, err = quad_vec(f, 0, 1, args=extra_args, workers=workers)
    assert_allclose(res, exact, rtol=0, atol=1e-4)

    with Pool(workers) as pool:
        res, err = quad_vec(f, 0, 1, args=extra_args, workers=pool.map)
        assert_allclose(res, exact, rtol=0, atol=1e-4)
