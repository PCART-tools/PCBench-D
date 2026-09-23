def test_itemsize():
    x = da.ones((10, 2), chunks=(3, 1))
    assert x.itemsize == 8
