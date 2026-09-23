@pytest.mark.parametrize(
    'type_', [t for t in np.ScalarType if t not in [memoryview] +
              ([buffer] if PY2 else [])])  # noqa: F821
def test_from_array_scalar(type_):
    """Python and numpy scalars are automatically converted to ndarray
    """
    if type_ == np.datetime64:
        x = np.datetime64('2000-01-01')
    else:
        x = type_(1)

    dx = da.from_array(x, chunks=-1)
    assert_eq(np.array(x), dx)
    assert isinstance(dx.dask[dx.name, ], np.ndarray)
