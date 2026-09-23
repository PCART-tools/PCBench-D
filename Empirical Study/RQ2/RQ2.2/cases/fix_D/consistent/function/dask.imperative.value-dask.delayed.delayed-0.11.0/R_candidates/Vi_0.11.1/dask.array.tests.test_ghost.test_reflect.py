def test_reflect():
    x = np.arange(10)
    d = da.from_array(x, chunks=(5, 5))

    e = reflect(d, axis=0, depth=2)
    expected = np.array([1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8])
    assert_eq(e, expected)

    e = reflect(d, axis=0, depth=1)
    expected = np.array([0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9])
    assert_eq(e, expected)
