@pytest.mark.parametrize('ufunc', ['isreal', 'iscomplex', 'real', 'imag',
                                   'angle', 'fix'])
def test_ufunc_array_wrap(ufunc):
    """
    some np.ufuncs doesn't call __array_wrap__, it should work as below

    - da.ufunc(dd.Series) => dd.Series
    - da.ufunc(pd.Series) => np.ndarray
    - np.ufunc(dd.Series) => np.ndarray
    - np.ufunc(pd.Series) => np.ndarray
    """

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    s = pd.Series(np.random.randint(1, 100, size=20),
                  index=list('abcdefghijklmnopqrst'))
    ds = dd.from_pandas(s, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ds), dd.Series)
    assert_eq(dafunc(ds), pd.Series(npfunc(s), index=s.index))

    assert isinstance(npfunc(ds), np.ndarray)
    tm.assert_numpy_array_equal(npfunc(ds), npfunc(s))

    assert isinstance(dafunc(s), np.ndarray)
    tm.assert_numpy_array_equal(dafunc(s), npfunc(s))

    df = pd.DataFrame({'A': np.random.randint(1, 100, size=20),
                       'B': np.random.randint(1, 100, size=20),
                       'C': np.abs(np.random.randn(20))},
                      index=list('abcdefghijklmnopqrst'))
    ddf = dd.from_pandas(df, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ddf), dd.DataFrame)
    # result may be read-only ndarray
    exp = pd.DataFrame(npfunc(df).copy(), columns=df.columns, index=df.index)
    assert_eq(dafunc(ddf), exp)

    assert isinstance(npfunc(ddf), np.ndarray)
    tm.assert_numpy_array_equal(npfunc(ddf), npfunc(df))

    assert isinstance(dafunc(df), np.ndarray)
    tm.assert_numpy_array_equal(dafunc(df), npfunc(df))
