def test_Array_computation():
    a = Array({('x', 0, 0): np.eye(3)}, 'x', shape=(3, 3), chunks=(3, 3), dtype='f8')
    assert_eq(np.array(a), np.eye(3))
    assert isinstance(a.compute(), np.ndarray)
    assert float(a[0, 0]) == 1
