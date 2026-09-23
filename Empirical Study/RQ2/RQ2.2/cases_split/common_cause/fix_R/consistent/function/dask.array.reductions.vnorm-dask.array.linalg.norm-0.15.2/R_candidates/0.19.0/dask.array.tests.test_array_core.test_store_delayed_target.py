def test_store_delayed_target():
    from dask.delayed import delayed
    d = da.ones((4, 4), chunks=(2, 2))
    a, b = d + 1, d + 2

    # empty buffers to be used as targets
    targs = {}

    def make_target(key):
        a = np.empty((4, 4))
        targs[key] = a
        return a

    # delayed calls to these targets
    atd = delayed(make_target)('at')
    btd = delayed(make_target)('bt')

    # test not keeping result
    st = store([a, b], [atd, btd])

    at = targs['at']
    bt = targs['bt']

    assert st is None
    assert_eq(at, a)
    assert_eq(bt, b)

    # test keeping result
    for st_compute in [False, True]:
        targs.clear()

        st = store([a, b], [atd, btd], return_stored=True, compute=st_compute)
        if st_compute:
            assert all(
                not any(dask.core.get_deps(e.dask)[0].values()) for e in st
            )

        st = dask.compute(*st)

        at = targs['at']
        bt = targs['bt']

        assert st is not None
        assert isinstance(st, tuple)
        assert all([isinstance(v, np.ndarray) for v in st])
        assert_eq(at, a)
        assert_eq(bt, b)
        assert_eq(st[0], a)
        assert_eq(st[1], b)

        pytest.raises(ValueError, lambda: store([a], [at, bt]))
        pytest.raises(ValueError, lambda: store(at, at))
        pytest.raises(ValueError, lambda: store([at, bt], [at, bt]))
