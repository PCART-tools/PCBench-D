def test_store():
    d = da.ones((4, 4), chunks=(2, 2))
    a, b = d + 1, d + 2

    at = np.empty(shape=(4, 4))
    bt = np.empty(shape=(4, 4))

    st = store([a, b], [at, bt])
    assert st is None
    assert (at == 2).all()
    assert (bt == 3).all()

    pytest.raises(ValueError, lambda: store([a], [at, bt]))
    pytest.raises(ValueError, lambda: store(at, at))
    pytest.raises(ValueError, lambda: store([at, bt], [at, bt]))
