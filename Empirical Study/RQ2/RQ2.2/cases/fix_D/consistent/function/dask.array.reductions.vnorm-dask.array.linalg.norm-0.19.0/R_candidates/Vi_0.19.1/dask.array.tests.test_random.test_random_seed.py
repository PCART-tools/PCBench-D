def test_random_seed():
    da.random.seed(123)
    x = da.random.normal(size=10, chunks=5)
    y = da.random.normal(size=10, chunks=5)

    da.random.seed(123)
    a = da.random.normal(size=10, chunks=5)
    b = da.random.normal(size=10, chunks=5)

    assert_eq(x, a)
    assert_eq(y, b)
