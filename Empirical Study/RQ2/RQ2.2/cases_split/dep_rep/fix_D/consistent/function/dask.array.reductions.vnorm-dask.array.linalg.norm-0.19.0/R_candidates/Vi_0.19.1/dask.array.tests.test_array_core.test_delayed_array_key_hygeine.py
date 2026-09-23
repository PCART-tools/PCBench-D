def test_delayed_array_key_hygeine():
    a = da.zeros((1,), chunks=(1,))
    d = delayed(identity)(a)
    b = da.from_delayed(d, shape=a.shape, dtype=a.dtype)
    assert_eq(a, b)
