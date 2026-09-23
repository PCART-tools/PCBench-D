def test_store_regions():
    d = da.ones((4, 4, 4), dtype=int, chunks=(2, 2, 2))
    a, b = d + 1, d + 2
    a = a[:, 1:, :].astype(float)

    region = (slice(None, None, 2), slice(None), [1, 2, 4, 5])

    # Single region:
    at = np.zeros(shape=(8, 3, 6))
    bt = np.zeros(shape=(8, 4, 6))
    v = store([a, b], [at, bt], regions=region, compute=False)
    assert isinstance(v, Delayed)
    assert (at == 0).all() and (bt[region] == 0).all()
    assert all([ev is None for ev in v.compute()])
    assert (at[region] == 2).all() and (bt[region] == 3).all()
    assert not (bt == 3).all() and not ( bt == 0 ).all()
    assert not (at == 2).all() and not ( at == 0 ).all()

    # Multiple regions:
    at = np.zeros(shape=(8, 3, 6))
    bt = np.zeros(shape=(8, 4, 6))
    v = store([a, b], [at, bt], regions=[region, region], compute=False)
    assert isinstance(v, Delayed)
    assert (at == 0).all() and (bt[region] == 0).all()
    assert all([ev is None for ev in v.compute()])
    assert (at[region] == 2).all() and (bt[region] == 3).all()
    assert not (bt == 3).all() and not ( bt == 0 ).all()
    assert not (at == 2).all() and not ( at == 0 ).all()

    # Single region (keep result):
    for st_compute in [False, True]:
        at = np.zeros(shape=(8, 3, 6))
        bt = np.zeros(shape=(8, 4, 6))
        v = store(
            [a, b], [at, bt], regions=region,
            compute=st_compute, return_stored=True
        )
        assert isinstance(v, tuple)
        assert all([isinstance(e, da.Array) for e in v])
        if st_compute:
            assert all(
                not any(dask.core.get_deps(e.dask)[0].values()) for e in v
            )
        else:
            assert (at == 0).all() and (bt[region] == 0).all()

        ar, br = v
        assert ar.dtype == a.dtype
        assert br.dtype == b.dtype
        assert ar.shape == a.shape
        assert br.shape == b.shape
        assert ar.chunks == a.chunks
        assert br.chunks == b.chunks

        ar, br = da.compute(ar, br)
        assert (at[region] == 2).all() and (bt[region] == 3).all()
        assert not (bt == 3).all() and not ( bt == 0 ).all()
        assert not (at == 2).all() and not ( at == 0 ).all()
        assert (br == 3).all()
        assert (ar == 2).all()

    # Multiple regions (keep result):
    for st_compute in [False, True]:
        at = np.zeros(shape=(8, 3, 6))
        bt = np.zeros(shape=(8, 4, 6))
        v = store(
            [a, b], [at, bt], regions=[region, region],
            compute=st_compute, return_stored=True
        )
        assert isinstance(v, tuple)
        assert all([isinstance(e, da.Array) for e in v])
        if st_compute:
            assert all(
                not any(dask.core.get_deps(e.dask)[0].values()) for e in v
            )
        else:
            assert (at == 0).all() and (bt[region] == 0).all()

        ar, br = v
        assert ar.dtype == a.dtype
        assert br.dtype == b.dtype
        assert ar.shape == a.shape
        assert br.shape == b.shape
        assert ar.chunks == a.chunks
        assert br.chunks == b.chunks

        ar, br = da.compute(ar, br)
        assert (at[region] == 2).all() and (bt[region] == 3).all()
        assert not (bt == 3).all() and not ( bt == 0 ).all()
        assert not (at == 2).all() and not ( at == 0 ).all()
        assert (br == 3).all()
        assert (ar == 2).all()
