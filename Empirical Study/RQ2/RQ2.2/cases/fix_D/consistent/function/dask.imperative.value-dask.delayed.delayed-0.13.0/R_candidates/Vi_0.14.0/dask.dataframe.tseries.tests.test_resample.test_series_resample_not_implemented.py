def test_series_resample_not_implemented():
    index = pd.date_range(start='20120102', periods=100, freq='T')
    s = pd.Series(range(len(index)), index=index)
    ds = dd.from_pandas(s, npartitions=5)
    # Frequency doesn't evenly divide day
    pytest.raises(NotImplementedError, lambda: resample(ds, '57T'))
