def test_operator_dtype_promotion():
    x = np.arange(10, dtype=np.float32)
    y = np.array([1])
    a = from_array(x, chunks=(5,))

    assert_eq(x + 1, a + 1)  # still float32
    assert_eq(x + 1e50, a + 1e50)  # now float64
    assert_eq(x + y, a + y)  # also float64
