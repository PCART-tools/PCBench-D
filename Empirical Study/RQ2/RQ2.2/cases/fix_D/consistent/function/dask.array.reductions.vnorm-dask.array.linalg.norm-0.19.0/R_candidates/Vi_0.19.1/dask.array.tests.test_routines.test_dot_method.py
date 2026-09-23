def test_dot_method():
    x = np.arange(400).reshape((20, 20))
    a = da.from_array(x, chunks=(5, 5))
    y = np.arange(200).reshape((20, 10))
    b = da.from_array(y, chunks=(5, 5))

    assert_eq(a.dot(b), x.dot(y))
