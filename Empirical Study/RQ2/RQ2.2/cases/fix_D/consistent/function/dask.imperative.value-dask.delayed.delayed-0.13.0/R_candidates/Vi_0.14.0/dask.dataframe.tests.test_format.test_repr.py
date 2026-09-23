def test_repr():
    df = pd.DataFrame({'x': list(range(100))})
    ddf = dd.from_pandas(df, 3)

    for x in [ddf, ddf.index, ddf.x]:
        assert type(x).__name__ in repr(x)
        assert str(x.npartitions) in repr(x)
