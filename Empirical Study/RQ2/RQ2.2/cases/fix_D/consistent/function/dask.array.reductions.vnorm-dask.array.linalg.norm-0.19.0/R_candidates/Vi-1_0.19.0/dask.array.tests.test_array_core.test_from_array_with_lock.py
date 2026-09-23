def test_from_array_with_lock():
    x = np.arange(10)
    d = da.from_array(x, chunks=5, lock=True)

    tasks = [v for k, v in d.dask.items() if k[0] == d.name]

    assert hasattr(tasks[0][4], 'acquire')
    assert len(set(task[4] for task in tasks)) == 1

    assert_eq(d, x)

    lock = Lock()
    e = da.from_array(x, chunks=5, lock=lock)
    f = da.from_array(x, chunks=5, lock=lock)

    assert_eq(e + f, x + x)
