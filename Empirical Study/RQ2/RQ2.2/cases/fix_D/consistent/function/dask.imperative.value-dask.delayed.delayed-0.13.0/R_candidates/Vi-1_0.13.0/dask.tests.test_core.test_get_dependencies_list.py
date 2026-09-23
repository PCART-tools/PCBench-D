def test_get_dependencies_list():
    dsk = {'x': 1, 'y': 2, 'z': ['x', [(inc, 'y')]]}
    assert get_dependencies(dsk, 'z') == set(['x', 'y'])
    assert sorted(get_dependencies(dsk, 'z', as_list=True)) == ['x', 'y']
