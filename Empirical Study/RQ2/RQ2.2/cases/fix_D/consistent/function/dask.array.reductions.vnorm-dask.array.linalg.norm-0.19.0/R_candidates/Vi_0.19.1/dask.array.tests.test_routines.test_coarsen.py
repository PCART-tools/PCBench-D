def test_coarsen():
    x = np.random.randint(10, size=(24, 24))
    d = da.from_array(x, chunks=(4, 8))

    assert_eq(da.chunk.coarsen(np.sum, x, {0: 2, 1: 4}),
              da.coarsen(np.sum, d, {0: 2, 1: 4}))
    assert_eq(da.chunk.coarsen(np.sum, x, {0: 2, 1: 4}),
              da.coarsen(da.sum, d, {0: 2, 1: 4}))
