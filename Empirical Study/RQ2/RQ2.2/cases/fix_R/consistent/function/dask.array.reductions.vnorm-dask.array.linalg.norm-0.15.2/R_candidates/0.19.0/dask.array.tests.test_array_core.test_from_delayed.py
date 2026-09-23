def test_from_delayed():
    v = delayed(np.ones)((5, 3))
    x = from_delayed(v, shape=(5, 3), dtype=np.ones(0).dtype)
    assert isinstance(x, Array)
    assert_eq(x, np.ones((5, 3)))
