@pytest.mark.xfail(reason="can't lock with multiprocessing")
def test_store_multiprocessing_lock():
    d = da.ones((10, 10), chunks=(2, 2))
    a = d + 1

    at = np.zeros(shape=(10, 10))
    st = a.store(at, scheduler='processes', num_workers=10)
    assert st is None
