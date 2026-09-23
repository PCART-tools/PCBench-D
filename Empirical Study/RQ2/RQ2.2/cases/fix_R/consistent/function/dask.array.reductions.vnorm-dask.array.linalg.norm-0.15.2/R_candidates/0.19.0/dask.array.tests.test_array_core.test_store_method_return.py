def test_store_method_return():
    d = da.ones((10, 10), chunks=(2, 2))
    a = d + 1

    for compute in [False, True]:
        for return_stored in [False, True]:
            at = np.zeros(shape=(10, 10))
            r = a.store(
                at, scheduler='threads',
                compute=compute, return_stored=return_stored
            )

            if return_stored:
                assert isinstance(r, Array)
            elif compute:
                assert r is None
            else:
                assert isinstance(r, Delayed)
