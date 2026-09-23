def test_daily_stock():
    pytest.importorskip('pandas_datareader')
    df = dd.demo.daily_stock('GOOG', start='2010-01-01', stop='2010-01-30', freq='1h')
    assert isinstance(df, dd.DataFrame)
    assert 10 < df.npartitions < 31
    assert_eq(df, df)
