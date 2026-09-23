def test_mixed_output_type():
    y = da.random.random((10, 10), chunks=(5, 5))
    y[y < 0.8] = 0
    y = y.map_blocks(sparse.COO.from_numpy)

    x = da.zeros((10, 1), chunks=(5, 1))

    z = da.concatenate([x, y], axis=1)

    assert z.shape == (10, 11)

    zz = z.compute()
    assert isinstance(zz, sparse.COO)
    assert zz.nnz == y.compute().nnz
