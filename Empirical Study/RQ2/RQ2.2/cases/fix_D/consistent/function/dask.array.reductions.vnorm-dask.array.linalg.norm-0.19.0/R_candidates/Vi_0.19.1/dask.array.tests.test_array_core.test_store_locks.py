def test_store_locks():
    _Lock = type(Lock())
    d = da.ones((10, 10), chunks=(2, 2))
    a, b = d + 1, d + 2

    at = np.zeros(shape=(10, 10))
    bt = np.zeros(shape=(10, 10))

    lock = Lock()
    v = store([a, b], [at, bt], compute=False, lock=lock)
    assert isinstance(v, Delayed)
    dsk = v.dask
    locks = set(vv for v in dsk.values() for vv in v if isinstance(vv, _Lock))
    assert locks == set([lock])

    # Ensure same lock applies over multiple stores
    at = NonthreadSafeStore()
    v = store([a, b], [at, at], lock=lock,
              scheduler='threads', num_workers=10)
    assert v is None

    # Don't assume thread safety by default
    at = NonthreadSafeStore()
    assert store(a, at, scheduler='threads', num_workers=10) is None
    assert a.store(at, scheduler='threads', num_workers=10) is None

    # Ensure locks can be removed
    at = ThreadSafeStore()
    for i in range(10):
        st = a.store(at, lock=False, scheduler='threads', num_workers=10)
        assert st is None
        if at.max_concurrent_uses > 1:
            break
        if i == 9:
            assert False

    # Verify number of lock calls
    nchunks = np.sum([np.prod([len(c) for c in e.chunks]) for e in [a, b]])
    for c in (False, True):
        at = np.zeros(shape=(10, 10))
        bt = np.zeros(shape=(10, 10))
        lock = CounterLock()

        v = store([a, b], [at, bt], lock=lock, compute=c, return_stored=True)
        assert all(isinstance(e, Array) for e in v)

        da.compute(v)

        # When `return_stored=True` and `compute=False`,
        # the lock should be acquired only once for store and load steps
        # as they are fused together into one step.
        assert lock.acquire_count == lock.release_count
        if c:
            assert lock.acquire_count == 2 * nchunks
        else:
            assert lock.acquire_count == nchunks
