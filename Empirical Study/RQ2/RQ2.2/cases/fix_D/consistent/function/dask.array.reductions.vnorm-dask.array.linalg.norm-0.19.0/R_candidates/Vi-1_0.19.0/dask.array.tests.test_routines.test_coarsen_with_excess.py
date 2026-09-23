def test_coarsen_with_excess():
    x = da.arange(10, chunks=5)
    assert_eq(da.coarsen(np.min, x, {0: 3}, trim_excess=True),
              np.array([0, 5]))
    assert_eq(da.coarsen(np.sum, x, {0: 3}, trim_excess=True),
              np.array([0 + 1 + 2, 5 + 6 + 7]))
