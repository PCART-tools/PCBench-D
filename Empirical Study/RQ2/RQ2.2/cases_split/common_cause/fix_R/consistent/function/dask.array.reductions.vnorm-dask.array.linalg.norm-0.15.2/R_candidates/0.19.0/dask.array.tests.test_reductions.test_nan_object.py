@pytest.mark.skipif(np.__version__ < '1.13.0', reason='nanmax/nanmin for object dtype')
@pytest.mark.parametrize('func', ['nansum', 'sum', 'nanmin', 'min',
                                  'nanmax', 'max'])
def test_nan_object(func):
    x = np.array([[1, np.nan, 3, 4],
                  [5, 6, 7, np.nan],
                  [9, 10, 11, 12]]).astype(object)
    d = da.from_array(x, chunks=(2, 2))

    assert_eq(getattr(np, func)(x, axis=0), getattr(da, func)(d, axis=0))
    assert_eq(getattr(np, func)(x, axis=1), getattr(da, func)(d, axis=1))
    assert_eq(getattr(np, func)(x), getattr(da, func)(d))
