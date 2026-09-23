def test_index_format():
    s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8],
                  index=list('ABCDEFGH'))
    ds = dd.from_pandas(s, 3)
    exp = """Dask Index Structure:
npartitions=3
A    object
D       ...
G       ...
H       ...
dtype: object
Dask Name: from_pandas, 6 tasks"""
    assert repr(ds.index) == exp
    assert str(ds.index) == exp

    s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8],
                  index=pd.CategoricalIndex([1, 2, 3, 4, 5, 6, 7, 8], name='YYY'))
    ds = dd.from_pandas(s, 3)
    exp = """Dask Index Structure:
npartitions=3
1    category[known]
4                ...
7                ...
8                ...
Name: YYY, dtype: category
Dask Name: from_pandas, 6 tasks"""
    assert repr(ds.index) == exp
    assert str(ds.index) == exp
