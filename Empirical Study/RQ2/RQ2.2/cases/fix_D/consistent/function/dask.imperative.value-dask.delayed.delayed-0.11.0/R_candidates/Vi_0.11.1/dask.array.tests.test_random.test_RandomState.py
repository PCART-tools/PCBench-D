def test_RandomState():
    state = da.random.RandomState(5)
    x = state.normal(10, 1, size=10, chunks=5)
    assert (x.compute() == x.compute()).all()

    state = da.random.RandomState(5)
    y = state.normal(10, 1, size=10, chunks=5)
    assert (x.compute() == y.compute()).all()
