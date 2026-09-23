def test_elemwise_differently_chunked():
    x = np.arange(3)
    y = np.arange(12).reshape(4, 3)
    a = from_array(x, chunks=(3,))
    b = from_array(y, chunks=(2, 2))

    assert_eq(a + b, x + y)
    assert_eq(b + a, x + y)
