def test_RandomState():
    state = da.random.RandomState(5)
    x = state.normal(10, 1, size=10, chunks=5)
    assert_eq(x, x)

    state = da.random.RandomState(5)
    y = state.normal(10, 1, size=10, chunks=5)
    assert_eq(x, y)
