def test_consistent_across_sizes():
    x1 = da.random.RandomState(123).random(20, chunks=20)
    x2 = da.random.RandomState(123).random(100, chunks=20)[:20]
    x3 = da.random.RandomState(123).random(200, chunks=20)[:20]
    assert_eq(x1, x2)
    assert_eq(x1, x3)
