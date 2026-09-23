@pytest.mark.parametrize('compute', [False, True])
def test_zarr_return_stored(compute):
    pytest.importorskip('zarr')
    with tmpdir() as d:
        a = da.zeros((3, 3), chunks=(1, 1))
        a2 = a.to_zarr(d, compute=compute, return_stored=True)
        assert isinstance(a2, Array)
        assert_eq(a, a2)
        assert a2.chunks == a.chunks
