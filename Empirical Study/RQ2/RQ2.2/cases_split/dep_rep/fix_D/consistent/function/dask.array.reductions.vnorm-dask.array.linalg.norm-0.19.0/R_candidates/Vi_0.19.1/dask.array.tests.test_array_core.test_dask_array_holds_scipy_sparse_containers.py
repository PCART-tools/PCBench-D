def test_dask_array_holds_scipy_sparse_containers():
    pytest.importorskip('scipy.sparse')
    import scipy.sparse
    x = da.random.random((1000, 10), chunks=(100, 10))
    x[x < 0.9] = 0
    xx = x.compute()
    y = x.map_blocks(scipy.sparse.csr_matrix)

    vs = y.to_delayed().flatten().tolist()
    values = dask.compute(*vs, scheduler='single-threaded')
    assert all(isinstance(v, scipy.sparse.csr_matrix) for v in values)

    yy = y.compute(scheduler='single-threaded')
    assert isinstance(yy, scipy.sparse.spmatrix)
    assert (yy == xx).all()

    z = x.T.map_blocks(scipy.sparse.csr_matrix)
    zz = z.compute(scheduler='single-threaded')
    assert isinstance(yy, scipy.sparse.spmatrix)
    assert (zz == xx.T).all()
