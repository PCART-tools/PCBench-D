def test_gh3937():
    # test for github issue #3937
    x = da.from_array([1, 2, 3.], (2,))
    x = da.concatenate((x, [x[-1]]))
    y = x.rechunk((2,))
    # This will produce Integral type indices that are not ints (np.int64), failing
    # the optimizer
    y = da.coarsen(np.sum, y, {0: 2})
    # How to trigger the optimizer explicitly?
    y.compute()
