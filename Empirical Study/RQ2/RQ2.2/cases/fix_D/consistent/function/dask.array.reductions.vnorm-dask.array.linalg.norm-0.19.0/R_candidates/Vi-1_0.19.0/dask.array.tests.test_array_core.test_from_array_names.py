def test_from_array_names():
    pytest.importorskip('distributed')

    x = np.ones(10)
    d = da.from_array(x, chunks=2)

    names = countby(key_split, d.dask)
    assert set(names.values()) == set([1, 5])
