def test_clip():

    # clip internally calls dd.Series.clip

    s = pd.Series(np.random.randint(1, 100, size=20))
    ds = dd.from_pandas(s, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(da.clip(ds, 5, 50), dd.Series)
    assert_eq(da.clip(ds, 5, 50), np.clip(s, 5, 50))

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(np.clip(ds, 5, 50), dd.Series)
    assert_eq(np.clip(ds, 5, 50), np.clip(s, 5, 50))

    # applying Dask ufunc to normal Series triggers computation
    assert isinstance(da.clip(s, 5, 50), pd.Series)
    assert_eq(da.clip(s, 5, 50), np.clip(s, 5, 50))

    df = pd.DataFrame(np.random.randint(1, 100, size=(20, 2)),
                      columns=['A', 'B'])
    ddf = dd.from_pandas(df, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(da.clip(ddf, 5.5, 40.5), dd.DataFrame)
    assert_eq(da.clip(ddf, 5.5, 40.5), np.clip(df, 5.5, 40.5))

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(np.clip(ddf, 5.5, 40.5), dd.DataFrame)
    assert_eq(np.clip(ddf, 5.5, 40.5), np.clip(df, 5.5, 40.5))

    # applying Dask ufunc to normal DataFrame triggers computation
    assert isinstance(da.clip(df, 5.5, 40.5), pd.DataFrame)
    assert_eq(da.clip(df, 5.5, 40.5), np.clip(df, 5.5, 40.5))
