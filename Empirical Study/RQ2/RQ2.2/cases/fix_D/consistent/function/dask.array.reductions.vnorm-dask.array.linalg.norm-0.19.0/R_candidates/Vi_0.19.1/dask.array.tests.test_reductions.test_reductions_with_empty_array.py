def test_reductions_with_empty_array():
    dx1 = da.ones((10, 0, 5), chunks=4)
    x1 = dx1.compute()
    dx2 = da.ones((0, 0, 0), chunks=4)
    x2 = dx2.compute()

    for dx, x in [(dx1, x1), (dx2, x2)]:
        with pytest.warns(None):  # empty slice warning
            assert_eq(dx.mean(), x.mean())
            assert_eq(dx.mean(axis=0), x.mean(axis=0))
            assert_eq(dx.mean(axis=1), x.mean(axis=1))
            assert_eq(dx.mean(axis=2), x.mean(axis=2))
