def test_elemwise_consistent_names():
    a = da.from_array(np.arange(5, dtype='f4'), chunks=(2,))
    b = da.from_array(np.arange(5, dtype='f4'), chunks=(2,))
    assert same_keys(a + b, a + b)
    assert same_keys(a + 2, a + 2)
    assert same_keys(da.exp(a), da.exp(a))
    assert same_keys(da.exp(a, dtype='f8'), da.exp(a, dtype='f8'))
    assert same_keys(da.maximum(a, b), da.maximum(a, b))
