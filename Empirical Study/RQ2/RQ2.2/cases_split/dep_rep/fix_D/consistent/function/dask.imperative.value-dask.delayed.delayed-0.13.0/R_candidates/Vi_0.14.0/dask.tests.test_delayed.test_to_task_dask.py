def test_to_task_dask():
    a = delayed(1, name='a')
    b = delayed(2, name='b')
    task, dask = to_task_dask([a, b, 3])
    assert task == ['a', 'b', 3]

    task, dask = to_task_dask((a, b, 3))
    assert task == (tuple, ['a', 'b', 3])
    assert dict(dask) == merge(a.dask, b.dask)

    task, dask = to_task_dask({a: 1, b: 2})
    assert (task == (dict, [['b', 2], ['a', 1]]) or
            task == (dict, [['a', 1], ['b', 2]]))
    assert dict(dask) == merge(a.dask, b.dask)

    f = namedtuple('f', ['x', 'y'])
    x = f(1, 2)
    task, dask = to_task_dask(x)
    assert task == x
    assert dict(dask) == {}
