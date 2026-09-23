@pytest.mark.parametrize('ufunc', _BASE_UFUNCS)
def test_ufunc_with_index(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    s = pd.Series(np.random.randint(1, 100, size=20),
                  index=list('abcdefghijklmnopqrst'))
    ds = dd.from_pandas(s, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ds), dd.Series)
    assert_eq(dafunc(ds), npfunc(s))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ds), pd.Series)
    assert_eq(npfunc(ds), npfunc(s))

    # applying Dask ufunc to normal Series triggers computation
    assert isinstance(dafunc(s), pd.Series)
    assert_eq(dafunc(s), npfunc(s))

    s = pd.Series(np.abs(np.random.randn(20)),
                  index=list('abcdefghijklmnopqrst'))
    ds = dd.from_pandas(s, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ds), dd.Series)
    assert_eq(dafunc(ds), npfunc(s))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ds), pd.Series)
    assert_eq(npfunc(ds), npfunc(s))

    # applying Dask ufunc to normal Series triggers computation
    assert isinstance(dafunc(s), pd.Series)
    assert_eq(dafunc(s), npfunc(s))

    df = pd.DataFrame({'A': np.random.randint(1, 100, size=20),
                       'B': np.random.randint(1, 100, size=20),
                       'C': np.abs(np.random.randn(20))},
                      index=list('abcdefghijklmnopqrst'))
    ddf = dd.from_pandas(df, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ddf), dd.DataFrame)
    assert_eq(dafunc(ddf), npfunc(df))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ddf), pd.DataFrame)
    assert_eq(npfunc(ddf), npfunc(df))

    # applying Dask ufunc to normal DataFrame triggers computation
    assert isinstance(dafunc(df), pd.DataFrame)
    assert_eq(dafunc(df), npfunc(df))
