def test_series_format():
    s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8],
                  index=list('ABCDEFGH'))
    ds = dd.from_pandas(s, 3)
    exp = """Dask Series Structure:
npartitions=3
A    int64
D      ...
G      ...
H      ...
dtype: int64
Dask Name: from_pandas, 3 tasks"""
    assert repr(ds) == exp
    assert str(ds) == exp

    exp = """npartitions=3
A    int64
D      ...
G      ...
H      ..."""
    assert ds.to_string() == exp

    s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8],
                  index=list('ABCDEFGH'), name='XXX')
    ds = dd.from_pandas(s, 3)
    exp = """Dask Series Structure:
npartitions=3
A    int64
D      ...
G      ...
H      ...
Name: XXX, dtype: int64
Dask Name: from_pandas, 3 tasks"""
    assert repr(ds) == exp
    assert str(ds) == exp
