def test_delayed_picklable():
    x = delayed(1)
    y = pickle.loads(pickle.dumps(x))
    assert x.dask == y.dask
    assert x._key == y._key
