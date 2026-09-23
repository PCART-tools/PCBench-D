def test_size():
    x = da.ones((10, 2), chunks=(3, 1))
    assert x.size == np.array(x).size
    assert isinstance(x.size, int)
