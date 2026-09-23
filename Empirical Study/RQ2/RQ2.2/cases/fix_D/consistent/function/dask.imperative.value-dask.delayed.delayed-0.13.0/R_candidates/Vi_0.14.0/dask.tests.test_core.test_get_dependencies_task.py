def test_get_dependencies_task():
    dsk = {'x': 1, 'y': 2, 'z': ['x', [(inc, 'y')]]}
    assert get_dependencies(dsk, task=(inc, 'x')) == set(['x'])
    assert get_dependencies(dsk, task=(inc, 'x'), as_list=True) == ['x']
