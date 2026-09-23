def test_concatenate_unknown_axes():
    dd = pytest.importorskip('dask.dataframe')
    pd = pytest.importorskip('pandas')

    a_df = pd.DataFrame({'x': np.arange(12)})
    b_df = pd.DataFrame({'y': np.arange(12) * 10})

    a_ddf = dd.from_pandas(a_df, sort=False, npartitions=3)
    b_ddf = dd.from_pandas(b_df, sort=False, npartitions=3)

    a_x = a_ddf.values
    b_x = b_ddf.values

    assert np.isnan(a_x.shape[0])
    assert np.isnan(b_x.shape[0])

    da.concatenate([a_x, b_x], axis=0)  # works fine

    with pytest.raises(ValueError) as exc_info:
        da.concatenate([a_x, b_x], axis=1)  # unknown chunks

    assert 'nan' in str(exc_info.value)
    assert 'allow_unknown_chunksize' in str(exc_info.value)

    c_x = da.concatenate([a_x, b_x], axis=1, allow_unknown_chunksizes=True)  # unknown chunks

    assert_eq(c_x, np.concatenate([a_df.values, b_df.values], axis=1))
