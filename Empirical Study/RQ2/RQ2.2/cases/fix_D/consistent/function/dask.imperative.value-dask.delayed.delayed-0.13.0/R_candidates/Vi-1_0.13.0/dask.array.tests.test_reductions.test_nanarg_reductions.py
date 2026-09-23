@pytest.mark.parametrize(['dfunc', 'func'],
                         [(da.nanargmin, np.nanargmin),
                          (da.nanargmax, np.nanargmax)])
def test_nanarg_reductions(dfunc, func):
    x = np.random.random((10, 10, 10))
    x[5] = np.nan
    a = da.from_array(x, chunks=(3, 4, 5))
    assert_eq(dfunc(a), func(x))
    assert_eq(dfunc(a, 0), func(x, 0))
    with pytest.raises(ValueError):
        dfunc(a, 1).compute()

    with pytest.raises(ValueError):
        dfunc(a, 2).compute()

    x[:] = np.nan
    a = da.from_array(x, chunks=(3, 4, 5))
    with pytest.raises(ValueError):
        dfunc(a).compute()
