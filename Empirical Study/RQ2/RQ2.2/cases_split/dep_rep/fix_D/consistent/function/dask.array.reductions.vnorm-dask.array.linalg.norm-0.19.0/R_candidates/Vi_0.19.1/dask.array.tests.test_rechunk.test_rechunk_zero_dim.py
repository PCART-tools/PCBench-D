def test_rechunk_zero_dim():
    da = pytest.importorskip('dask.array')

    x = da.ones((0, 10, 100), chunks=(0, 10, 10)).rechunk((0, 10, 50))
    assert len(x.compute()) == 0
