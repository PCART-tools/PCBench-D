def test_isclose():
    x = np.array([0, np.nan, 1, 1.5])
    y = np.array([1e-9, np.nan, 1, 2])
    a = da.from_array(x, chunks=(2,))
    b = da.from_array(y, chunks=(2,))
    assert_eq(da.isclose(a, b, equal_nan=True),
              np.isclose(x, y, equal_nan=True))
