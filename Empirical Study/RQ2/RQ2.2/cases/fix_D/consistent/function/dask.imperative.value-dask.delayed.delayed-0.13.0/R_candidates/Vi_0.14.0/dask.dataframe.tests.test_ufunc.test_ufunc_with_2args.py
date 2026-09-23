@pytest.mark.parametrize('ufunc', ['logaddexp', 'logaddexp2', 'arctan2',
                                   'hypot', 'copysign', 'nextafter', 'ldexp',
                                   'fmod', 'logical_and', 'logical_or',
                                   'logical_xor', 'maximum', 'minimum',
                                   'fmax', 'fmin'])
def test_ufunc_with_2args(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    s1 = pd.Series(np.random.randint(1, 100, size=20))
    ds1 = dd.from_pandas(s1, 3)

    s2 = pd.Series(np.random.randint(1, 100, size=20))
    ds2 = dd.from_pandas(s2, 4)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ds1, ds2), dd.Series)
    assert_eq(dafunc(ds1, ds2), npfunc(s1, s2))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ds1, ds2), pd.Series)
    assert_eq(npfunc(ds1, ds2), npfunc(s1, s2))

    # applying Dask ufunc to normal Series triggers computation
    assert isinstance(dafunc(s1, s2), pd.Series)
    assert_eq(dafunc(s1, s2), npfunc(s1, s2))

    df1 = pd.DataFrame(np.random.randint(1, 100, size=(20, 2)),
                       columns=['A', 'B'])
    ddf1 = dd.from_pandas(df1, 3)

    df2 = pd.DataFrame(np.random.randint(1, 100, size=(20, 2)),
                       columns=['A', 'B'])
    ddf2 = dd.from_pandas(df2, 4)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(ddf1, ddf2), dd.DataFrame)
    assert_eq(dafunc(ddf1, ddf2), npfunc(df1, df2))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(ddf1, ddf2), pd.DataFrame)
    assert_eq(npfunc(ddf1, ddf2), npfunc(df1, df2))

    # applying Dask ufunc to normal DataFrame triggers computation
    assert isinstance(dafunc(df1, df2), pd.DataFrame)
    assert_eq(dafunc(df1, df2), npfunc(df1, df2))
