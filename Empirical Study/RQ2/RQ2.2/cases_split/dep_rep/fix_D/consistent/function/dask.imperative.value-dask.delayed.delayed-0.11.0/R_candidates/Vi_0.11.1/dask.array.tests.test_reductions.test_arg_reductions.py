@pytest.mark.parametrize(['dfunc', 'func'],
        [(da.argmin, np.argmin), (da.argmax, np.argmax),
         (da.nanargmin, np.nanargmin), (da.nanargmax, np.nanargmax)])
def test_arg_reductions(dfunc, func):
    x = np.random.random((10, 10, 10))
    a = da.from_array(x, chunks=(3, 4, 5))

    assert_eq(dfunc(a), func(x))
    assert_eq(dfunc(a, 0), func(x, 0))
    assert_eq(dfunc(a, 1), func(x, 1))
    assert_eq(dfunc(a, 2), func(x, 2))
    with set_options(split_every=2):
        assert_eq(dfunc(a), func(x))
        assert_eq(dfunc(a, 0), func(x, 0))
        assert_eq(dfunc(a, 1), func(x, 1))
        assert_eq(dfunc(a, 2), func(x, 2))

    pytest.raises(ValueError, lambda: dfunc(a, 3))
    pytest.raises(TypeError, lambda: dfunc(a, (0, 1)))

    x2 = np.arange(10)
    a2 = da.from_array(x2, chunks=3)
    assert_eq(dfunc(a2), func(x2))
    assert_eq(dfunc(a2, 0), func(x2, 0))
    assert_eq(dfunc(a2, 0, split_every=2), func(x2, 0))
