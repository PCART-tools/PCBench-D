def test_nbytes():
    x = da.ones((10, 2), chunks=(3, 1))
    assert x.nbytes == np.array(x).nbytes
