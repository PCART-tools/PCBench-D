def test_zarr_roundtrip():
    pytest.importorskip('zarr')
    with tmpdir() as d:
        a = da.zeros((3, 3), chunks=(1, 1))
        a.to_zarr(d)
        a2 = da.from_zarr(d)
        assert_eq(a, a2)
        assert a2.chunks == a.chunks
