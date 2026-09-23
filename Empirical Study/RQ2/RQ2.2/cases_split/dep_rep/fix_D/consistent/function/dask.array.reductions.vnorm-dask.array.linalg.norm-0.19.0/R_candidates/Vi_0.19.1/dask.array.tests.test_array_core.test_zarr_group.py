def test_zarr_group():
    zarr = pytest.importorskip('zarr')
    with tmpdir() as d:
        a = da.zeros((3, 3), chunks=(1, 1))
        a.to_zarr(d, component='test')
        with pytest.raises((OSError, ValueError)):
            a.to_zarr(d, component='test', overwrite=False)
        a.to_zarr(d, component='test', overwrite=True)

        # second time is fine, group exists
        a.to_zarr(d, component='test2', overwrite=False)
        a.to_zarr(d, component='nested/test', overwrite=False)
        group = zarr.open_group(d, mode='r')
        assert list(group) == ['nested', 'test', 'test2']
        assert 'test' in group['nested']

        a2 = da.from_zarr(d, component='test')
        assert_eq(a, a2)
        assert a2.chunks == a.chunks
