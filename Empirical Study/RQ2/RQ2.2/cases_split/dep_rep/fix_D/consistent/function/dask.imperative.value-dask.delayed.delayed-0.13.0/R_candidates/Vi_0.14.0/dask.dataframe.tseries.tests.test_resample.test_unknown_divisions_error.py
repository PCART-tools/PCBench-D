def test_unknown_divisions_error():
    df = pd.DataFrame({'x': [1, 2, 3]})
    ddf = dd.from_pandas(df, npartitions=2, sort=False)
    try:
        ddf.x.resample('1m').mean()
        assert False
    except ValueError as e:
        assert 'divisions' in str(e)
