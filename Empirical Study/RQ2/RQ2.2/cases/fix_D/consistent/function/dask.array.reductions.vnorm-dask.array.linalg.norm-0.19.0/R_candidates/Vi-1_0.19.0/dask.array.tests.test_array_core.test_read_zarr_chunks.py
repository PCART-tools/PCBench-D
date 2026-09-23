def test_read_zarr_chunks():
    pytest.importorskip('zarr')
    a = da.zeros((9, ), chunks=(3, ))
    with tmpdir() as d:
        a.to_zarr(d)
        arr = da.from_zarr(d, chunks=(5, ))
        assert arr.chunks == ((5, 4), )
