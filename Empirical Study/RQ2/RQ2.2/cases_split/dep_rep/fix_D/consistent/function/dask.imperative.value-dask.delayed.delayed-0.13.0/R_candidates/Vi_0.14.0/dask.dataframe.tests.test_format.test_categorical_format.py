def test_categorical_format():
    s = pd.Series(['a', 'b', 'c']).astype('category')
    known = dd.from_pandas(s, npartitions=1)
    unknown = known.cat.as_unknown()
    exp = ("Dask Series Structure:\n"
           "npartitions=1\n"
           "0    category[known]\n"
           "2                ...\n"
           "dtype: category\n"
           "Dask Name: from_pandas, 1 tasks")
    assert repr(known) == exp
    exp = ("Dask Series Structure:\n"
           "npartitions=1\n"
           "0    category[unknown]\n"
           "2                  ...\n"
           "dtype: category\n"
           "Dask Name: from_pandas, 1 tasks")
    assert repr(unknown) == exp
