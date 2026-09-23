def test_np_array_with_zero_dimensions():
    d = da.ones((4, 4), chunks=(2, 2))
    assert_eq(np.array(d.sum()), np.array(d.compute().sum()))
