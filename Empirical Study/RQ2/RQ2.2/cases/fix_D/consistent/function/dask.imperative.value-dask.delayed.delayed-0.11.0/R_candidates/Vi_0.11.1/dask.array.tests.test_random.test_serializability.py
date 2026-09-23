def test_serializability():
    state = da.random.RandomState(5)
    x = state.normal(10, 1, size=10, chunks=5)

    y = _loads(_dumps(x))

    assert (x.compute() == y.compute()).all()
