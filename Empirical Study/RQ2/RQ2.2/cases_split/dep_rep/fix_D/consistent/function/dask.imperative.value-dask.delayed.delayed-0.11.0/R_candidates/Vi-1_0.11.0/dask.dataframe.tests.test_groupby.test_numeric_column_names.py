def test_numeric_column_names():
    # df.groupby(0)[df.columns] fails if all columns are numbers (pandas bug)
    # This ensures that we cast all column iterables to list beforehand.
    df = pd.DataFrame({0: [0, 1, 0, 1],
                       1: [1, 2, 3, 4]})
    ddf = dd.from_pandas(df, npartitions=2)
    eq(ddf.groupby(0).sum(), df.groupby(0).sum())
    eq(ddf.groupby(0).apply(lambda x: x), df.groupby(0).apply(lambda x: x))
