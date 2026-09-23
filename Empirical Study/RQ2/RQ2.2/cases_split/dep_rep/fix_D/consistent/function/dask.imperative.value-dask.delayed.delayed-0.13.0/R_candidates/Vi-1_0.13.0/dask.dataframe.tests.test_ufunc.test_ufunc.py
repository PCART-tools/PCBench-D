@pytest.mark.parametrize('ufunc', _BASE_UFUNCS)
def test_ufunc(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    s = pd.Series(np.random.randint(1, 100, size=20))
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

    s = pd.Series(np.abs(np.random.randn(100)))
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

    # DataFrame
    df = pd.DataFrame({'A': np.random.randint(1, 100, size=20),
                       'B': np.random.randint(1, 100, size=20),
                       'C': np.abs(np.random.randn(20))})
    ddf = dd.from_pandas(df, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ddf), dd.DataFrame)
    assert_eq(dafunc(ddf), npfunc(df))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ddf), pd.DataFrame)
    assert_eq(npfunc(ddf), npfunc(df))

    # applying Dask ufunc to normal Dataframe triggers computation
    assert isinstance(dafunc(df), pd.DataFrame)
    assert_eq(dafunc(df), npfunc(df))

    # Index
    if ufunc in ('logical_not', 'signbit', 'isnan', 'isinf', 'isfinite'):
        return

    assert isinstance(dafunc(ddf.index), dd.Index)
    assert_eq(dafunc(ddf.index), npfunc(df.index))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ddf.index), pd.Index)
    assert_eq(npfunc(ddf.index), npfunc(df.index))

    # applying Dask ufunc to normal Series triggers computation
    assert isinstance(dafunc(df.index), pd.Index)
    assert_eq(dafunc(df), npfunc(df))
