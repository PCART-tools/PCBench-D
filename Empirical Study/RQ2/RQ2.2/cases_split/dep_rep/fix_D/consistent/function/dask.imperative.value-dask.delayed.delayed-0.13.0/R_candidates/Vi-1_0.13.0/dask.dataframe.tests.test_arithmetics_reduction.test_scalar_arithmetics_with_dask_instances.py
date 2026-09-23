def test_scalar_arithmetics_with_dask_instances():
    s = dd.core.Scalar({('s', 0): 10}, 's', 'i8')
    e = 10

    pds = pd.Series([1, 2, 3, 4, 5, 6, 7])
    dds = dd.from_pandas(pds, 2)

    pdf = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7],
                        'b': [7, 6, 5, 4, 3, 2, 1]})
    ddf = dd.from_pandas(pdf, 2)

    # pandas Series
    result = pds + s   # this result pd.Series (automatically computed)
    assert isinstance(result, pd.Series)
    assert_eq(result, pds + e)

    result = s + pds   # this result dd.Series
    assert isinstance(result, dd.Series)
    assert_eq(result, pds + e)

    # dask Series
    result = dds + s   # this result dd.Series
    assert isinstance(result, dd.Series)
    assert_eq(result, pds + e)

    result = s + dds   # this result dd.Series
    assert isinstance(result, dd.Series)
    assert_eq(result, pds + e)

    # pandas DataFrame
    result = pdf + s   # this result pd.DataFrame (automatically computed)
    assert isinstance(result, pd.DataFrame)
    assert_eq(result, pdf + e)

    result = s + pdf   # this result dd.DataFrame
    assert isinstance(result, dd.DataFrame)
    assert_eq(result, pdf + e)

    # dask DataFrame
    result = ddf + s   # this result dd.DataFrame
    assert isinstance(result, dd.DataFrame)
    assert_eq(result, pdf + e)

    result = s + ddf   # this result dd.DataFrame
    assert isinstance(result, dd.DataFrame)
    assert_eq(result, pdf + e)
