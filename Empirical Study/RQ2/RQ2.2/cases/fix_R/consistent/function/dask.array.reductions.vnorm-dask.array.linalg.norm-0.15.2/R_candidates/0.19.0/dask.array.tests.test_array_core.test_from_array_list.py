@pytest.mark.parametrize(
    'x', [[1, 2], (1, 2), memoryview(b'abc')] +
    ([buffer(b'abc')] if PY2 else []))  # noqa: F821
def test_from_array_list(x):
    """Lists, tuples, and memoryviews are automatically converted to ndarray
    """
    dx = da.from_array(x, chunks=-1)
    assert_eq(np.array(x), dx)
    assert isinstance(dx.dask[dx.name, 0], np.ndarray)

    dx = da.from_array(x, chunks=1)
    assert_eq(np.array(x), dx)
    assert dx.dask[dx.name, 0][0] == operator.getitem
    assert isinstance(dx.dask[dx.name.replace('array', 'array-original')],
                      np.ndarray)
