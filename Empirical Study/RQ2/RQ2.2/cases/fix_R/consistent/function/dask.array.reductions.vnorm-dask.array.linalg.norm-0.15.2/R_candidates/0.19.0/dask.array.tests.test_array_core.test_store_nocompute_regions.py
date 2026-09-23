def test_store_nocompute_regions():
    x = da.ones(10, chunks=1)
    y = np.zeros((2, 10))
    d1 = da.store(x, y, regions=(0,), compute=False)
    d2 = da.store(x, y, regions=(1,), compute=False)
    assert d1.key != d2.key
