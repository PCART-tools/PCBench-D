def test_T():
    x = np.arange(400).reshape((20, 20))
    a = from_array(x, chunks=(5, 5))

    assert_eq(x.T, a.T)
