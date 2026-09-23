@pytest.mark.parametrize('dtype', ('i8', 'f8'))
@pytest.mark.parametrize('reduction', ['sum', 'prod', 'mean', 'var', 'std',
                                       'min', 'max', 'any', 'all'])
def test_reductions(dtype, reduction):
    x = (np.random.RandomState(42).rand(11, 11) * 10).astype(dtype)
    dx = da.from_array(x, chunks=(4, 4))
    mx = np.ma.masked_greater(x, 5)
    mdx = da.ma.masked_greater(dx, 5)

    dfunc = getattr(da, reduction)
    func = getattr(np, reduction)

    assert_eq_ma(dfunc(mdx), func(mx))
    assert_eq_ma(dfunc(mdx, axis=0), func(mx, axis=0))
    assert_eq_ma(dfunc(mdx, keepdims=True, split_every=4),
                 func(mx, keepdims=True))
    assert_eq_ma(dfunc(mdx, axis=0, split_every=2), func(mx, axis=0))
    assert_eq_ma(dfunc(mdx, axis=0, keepdims=True, split_every=2),
                 func(mx, axis=0, keepdims=True))
    assert_eq_ma(dfunc(mdx, axis=1, split_every=2), func(mx, axis=1))
    assert_eq_ma(dfunc(mdx, axis=1, keepdims=True, split_every=2),
                 func(mx, axis=1, keepdims=True))
