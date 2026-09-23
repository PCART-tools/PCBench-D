@pytest.mark.parametrize(['method', 'npartitions', 'freq', 'closed', 'label'],
                         list(product(['count', 'mean', 'ohlc'],
                                      [2, 5],
                                      ['30T', 'h', 'd', 'w', 'M'],
                                      ['right', 'left'],
                                      ['right', 'left'])))
def test_series_resample(method, npartitions, freq, closed, label):
    index = pd.date_range('1-1-2000', '2-15-2000', freq='h')
    index = index.union(pd.date_range('4-15-2000', '5-15-2000', freq='h'))
    ps = pd.Series(range(len(index)), index=index)
    ds = dd.from_pandas(ps, npartitions=npartitions)
    # Series output

    result = resample(ds, freq, how=method, closed=closed, label=label)
    expected = resample(ps, freq, how=method, closed=closed, label=label)
    eq(result, expected, check_dtype=False)

    divisions = result.divisions

    assert expected.index[0] == divisions[0]
    assert expected.index[-1] == divisions[-1]
