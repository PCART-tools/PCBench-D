def test_minimize_data_transfer():
    x = np.ones(100)
    y = da.from_array(x, chunks=25)
    z = y + 1
    dsk = z.__dask_optimize__(z.dask, z.__dask_keys__())

    keys = list(dsk)
    results = dask.get(dsk, keys)
    big_key = [k for k, r in zip(keys, results) if r is x][0]
    dependencies, dependents = dask.core.get_deps(dsk)
    deps = dependents[big_key]

    assert len(deps) == 4
    for dep in deps:
        assert dsk[dep][0] in (getitem, getter)
        assert dsk[dep][1] == big_key
