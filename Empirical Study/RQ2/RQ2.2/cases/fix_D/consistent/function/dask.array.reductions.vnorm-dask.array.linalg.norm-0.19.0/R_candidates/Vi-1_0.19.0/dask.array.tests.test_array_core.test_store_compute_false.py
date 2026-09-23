def test_store_compute_false():
    d = da.ones((4, 4), chunks=(2, 2))
    a, b = d + 1, d + 2

    at = np.zeros(shape=(4, 4))
    bt = np.zeros(shape=(4, 4))

    v = store([a, b], [at, bt], compute=False)
    assert isinstance(v, Delayed)
    assert (at == 0).all() and (bt == 0).all()
    assert all([ev is None for ev in v.compute()])
    assert (at == 2).all() and (bt == 3).all()

    at = np.zeros(shape=(4, 4))
    bt = np.zeros(shape=(4, 4))

    dat, dbt = store([a, b], [at, bt], compute=False, return_stored=True)
    assert isinstance(dat, Array) and isinstance(dbt, Array)
    assert (at == 0).all() and (bt == 0).all()
    assert (dat.compute() == at).all() and (dbt.compute() == bt).all()
    assert (at == 2).all() and (bt == 3).all()
