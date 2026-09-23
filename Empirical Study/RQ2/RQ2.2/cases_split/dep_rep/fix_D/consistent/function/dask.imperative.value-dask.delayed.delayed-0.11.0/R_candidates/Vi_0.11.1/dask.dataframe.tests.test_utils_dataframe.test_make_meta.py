def test_make_meta():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': list('abc'), 'c': [1., 2., 3.]},
                      index=[10, 20, 30])

    # Pandas dataframe
    meta = make_meta(df)
    assert len(meta) == 0
    assert (meta.dtypes == df.dtypes).all()
    assert isinstance(meta.index, type(df.index))

    # Pandas series
    meta = make_meta(df.a)
    assert len(meta) == 0
    assert meta.dtype == df.a.dtype
    assert isinstance(meta.index, type(df.index))

    # Pandas index
    meta = make_meta(df.index)
    assert isinstance(meta, type(df.index))
    assert len(meta) == 0

    # Dask object
    ddf = dd.from_pandas(df, npartitions=2)
    assert make_meta(ddf) is ddf._meta

    # Dict
    meta = make_meta({'a': 'i8', 'b': 'O', 'c': 'f8'})
    assert isinstance(meta, pd.DataFrame)
    assert len(meta) == 0
    assert (meta.dtypes == df.dtypes).all()
    assert isinstance(meta.index, pd.RangeIndex)

    # Iterable
    meta = make_meta([('a', 'i8'), ('c', 'f8'), ('b', 'O')])
    assert (meta.columns == ['a', 'c', 'b']).all()
    assert len(meta) == 0
    assert (meta.dtypes == df.dtypes[meta.dtypes.index]).all()
    assert isinstance(meta.index, pd.RangeIndex)

    # Tuple
    meta = make_meta(('a', 'i8'))
    assert isinstance(meta, pd.Series)
    assert len(meta) == 0
    assert meta.dtype == 'i8'
    assert meta.name == 'a'

    # With index
    meta = make_meta({'a': 'i8', 'b': 'i4'}, pd.Int64Index([1, 2], name='foo'))
    assert isinstance(meta.index, pd.Int64Index)
    assert len(meta.index) == 0
    meta = make_meta(('a', 'i8'), pd.Int64Index([1, 2], name='foo'))
    assert isinstance(meta.index, pd.Int64Index)
    assert len(meta.index) == 0

    # Numpy scalar
    meta = make_meta(np.float64(1.0))
    assert isinstance(meta, np.float64)

    # Python scalar
    meta = make_meta(1.0)
    assert isinstance(meta, np.float64)

    # Timestamp
    x = pd.Timestamp(2000, 1, 1)
    meta = make_meta(x)
    assert meta is x

    # Dtype expressions
    meta = make_meta('i8')
    assert isinstance(meta, np.int64)
    meta = make_meta(float)
    assert isinstance(meta, np.dtype(float).type)
    meta = make_meta(np.dtype('bool'))
    assert isinstance(meta, np.bool_)
    assert pytest.raises(TypeError, lambda: make_meta(None))
