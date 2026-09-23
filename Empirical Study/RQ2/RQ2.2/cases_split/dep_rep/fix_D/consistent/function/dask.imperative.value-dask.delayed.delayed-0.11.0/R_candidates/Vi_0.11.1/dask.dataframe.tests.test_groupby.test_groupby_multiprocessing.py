def test_groupby_multiprocessing():
    from dask.multiprocessing import get
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5],
                       'B': ['1','1','a','a','a']})
    ddf = dd.from_pandas(df, npartitions=3)
    with dask.set_options(get=get):
        assert eq(ddf.groupby('B').apply(lambda x: x),
                  df.groupby('B').apply(lambda x: x))
