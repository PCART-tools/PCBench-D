def test_zarr_pass_mapper():
    pytest.importorskip('zarr')
    import zarr.storage
    with tmpdir() as d:
        mapper = zarr.storage.DirectoryStore(d)
        a = da.zeros((3, 3), chunks=(1, 1))
        a.to_zarr(mapper)
        a2 = da.from_zarr(mapper)
        assert_eq(a, a2)
        assert a2.chunks == a.chunks
