def test_topk_argtopk3():
    a = da.random.random((10, 20, 30), chunks=(4, 8, 8))

    # As Array methods
    assert_eq(a.topk(5, axis=1, split_every=2),
              da.topk(a, 5, axis=1, split_every=2))
    assert_eq(a.argtopk(5, axis=1, split_every=2),
              da.argtopk(a, 5, axis=1, split_every=2))
