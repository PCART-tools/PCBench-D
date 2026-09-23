def test_elemwise_with_ndarrays():
    x = np.arange(3)
    y = np.arange(12).reshape(4, 3)
    a = from_array(x, chunks=(3,))
    b = from_array(y, chunks=(2, 3))

    assert_eq(x + a, 2 * x)
    assert_eq(a + x, 2 * x)

    assert_eq(x + b, x + y)
    assert_eq(b + x, x + y)
    assert_eq(a + y, x + y)
    assert_eq(y + a, x + y)
    # Error on shape mismatch
    pytest.raises(ValueError, lambda: a + y.T)
    pytest.raises(ValueError, lambda: a + np.arange(2))
