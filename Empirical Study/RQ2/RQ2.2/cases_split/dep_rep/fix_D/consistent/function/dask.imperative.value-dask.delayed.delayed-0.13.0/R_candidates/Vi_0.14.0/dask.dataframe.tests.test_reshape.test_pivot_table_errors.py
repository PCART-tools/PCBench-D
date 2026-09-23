def test_pivot_table_errors():
    df = pd.DataFrame({'A': np.random.choice(list('abc'), size=10),
                       'B': np.random.randn(10),
                       'C': pd.Categorical(np.random.choice(list('abc'), size=10))})
    ddf = dd.from_pandas(df, 2)

    msg = "'index' must be the name of an existing column"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index=['A'], columns='C', values='B')
    msg = "'columns' must be the name of an existing column"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns=['C'], values='B')
    msg = "'values' must be the name of an existing column"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns='C', values=['B'])

    msg = "aggfunc must be either 'mean', 'sum' or 'count'"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns='C', values='B', aggfunc=['sum'])

    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns='C', values='B', aggfunc='xx')

    # unknown categories
    ddf._meta = make_meta({'A': object, 'B': float, 'C': 'category'})
    msg = "'columns' must have known categories"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns='C', values=['B'])

    df = pd.DataFrame({'A': np.random.choice(list('abc'), size=10),
                       'B': np.random.randn(10),
                       'C': np.random.choice(list('abc'), size=10)})
    ddf = dd.from_pandas(df, 2)
    msg = "'columns' must be category dtype"
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.pivot_table(ddf, index='A', columns='C', values='B')
