def test_concurrency():
    state = da.random.RandomState(5)
    x = state.normal(10, 1, size=10, chunks=2)

    state = da.random.RandomState(5)
    y = state.normal(10, 1, size=10, chunks=2)
    assert (x.compute(get=mpget) == y.compute(get=mpget)).all()
