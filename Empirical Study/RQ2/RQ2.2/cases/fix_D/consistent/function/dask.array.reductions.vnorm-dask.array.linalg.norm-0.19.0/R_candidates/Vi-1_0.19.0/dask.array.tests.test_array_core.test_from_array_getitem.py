def test_from_array_getitem():
    x = np.arange(10)

    def my_getitem(x, ind):
        return x[ind]

    y = da.from_array(x, chunks=(5,), getitem=my_getitem)

    for k, v in y.dask.items():
        if isinstance(v, tuple):
            assert v[0] is my_getitem

    assert_eq(x, y)
