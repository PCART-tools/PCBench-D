def test_zarr_nocompute():
    pytest.importorskip('zarr')
    with tmpdir() as d:
        a = da.zeros((3, 3), chunks=(1, 1))
        out = a.to_zarr(d, compute=False)
        assert isinstance(out, Delayed)
        dask.compute(out)
        a2 = da.from_zarr(d)
        assert_eq(a, a2)
        assert a2.chunks == a.chunks
