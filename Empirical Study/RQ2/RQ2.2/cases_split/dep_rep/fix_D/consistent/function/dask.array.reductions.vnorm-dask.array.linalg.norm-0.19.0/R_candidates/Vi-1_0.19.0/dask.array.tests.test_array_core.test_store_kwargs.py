def test_store_kwargs():
    d = da.ones((10, 10), chunks=(2, 2))
    a = d + 1

    called = [False]

    def get_func(*args, **kwargs):
        assert kwargs.pop("foo") == "test kwarg"
        r = dask.get(*args, **kwargs)
        called[0] = True
        return r

    called[0] = False
    at = np.zeros(shape=(10, 10))
    store([a], [at], get=get_func, foo="test kwarg")
    assert called[0]

    called[0] = False
    at = np.zeros(shape=(10, 10))
    a.store(at, get=get_func, foo="test kwarg")
    assert called[0]

    called[0] = False
    at = np.zeros(shape=(10, 10))
    store([a], [at], get=get_func, return_store=True, foo="test kwarg")
    assert called[0]
