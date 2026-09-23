def test_to_task_dasks():
    a = delayed(1, name='a')
    b = delayed(2, name='b')
    task, dasks = to_task_dasks([a, b, 3])
    assert task == ['a', 'b', 3]
    assert len(dasks) == 2
    assert a.dask in dasks
    assert b.dask in dasks

    task, dasks = to_task_dasks((a, b, 3))
    assert task == (tuple, ['a', 'b', 3])
    assert len(dasks) == 2
    assert a.dask in dasks
    assert b.dask in dasks

    task, dasks = to_task_dasks({a: 1, b: 2})
    assert (task == (dict, [['b', 2], ['a', 1]]) or
            task == (dict, [['a', 1], ['b', 2]]))
    assert len(dasks) == 2
    assert a.dask in dasks
    assert b.dask in dasks

    f = namedtuple('f', ['x', 'y'])
    x = f(1, 2)
    task, dasks = to_task_dasks(x)
    assert task == x
    assert dasks == []
