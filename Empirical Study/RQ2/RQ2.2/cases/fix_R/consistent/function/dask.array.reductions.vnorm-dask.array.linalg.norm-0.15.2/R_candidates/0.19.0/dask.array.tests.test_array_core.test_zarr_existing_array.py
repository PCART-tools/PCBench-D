def test_zarr_existing_array():
    zarr = pytest.importorskip('zarr')
    c = (1, 1)
    a = da.ones((3, 3), chunks=c)
    z = zarr.zeros_like(a, chunks=c)
    a.to_zarr(z)
    a2 = da.from_zarr(z)
    assert_eq(a, a2)
    assert a2.chunks == a.chunks
