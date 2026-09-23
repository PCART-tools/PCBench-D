@pytest.mark.parametrize('chunks', [10, 5, 3])
def test_fuse_getter_with_asarray(chunks):
    x = np.ones(10) * 1234567890
    y = da.ones(10, chunks=chunks)
    z = x + y
    dsk = z.__dask_optimize__(z.dask, z.__dask_keys__())
    assert any(v is x for v in dsk.values())
    for v in dsk.values():
        s = str(v)
        assert s.count('getitem') + s.count('getter') <= 1
        if v is not x:
            assert '1234567890' not in s
    n_getters = len([v for v in dsk.values() if v[0] in (getitem, getter)])
    if y.npartitions > 1:
        assert n_getters == y.npartitions
    else:
        assert n_getters == 0

    assert_eq(z, x + 1)
