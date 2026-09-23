def test_multiple_list_slicing():
    x = np.random.rand(6, 7, 8)
    a = da.from_array(x, chunks=(3, 3, 3))
    assert_eq(x[:, [0, 1, 2]][[0, 1]], a[:, [0, 1, 2]][[0, 1]])
