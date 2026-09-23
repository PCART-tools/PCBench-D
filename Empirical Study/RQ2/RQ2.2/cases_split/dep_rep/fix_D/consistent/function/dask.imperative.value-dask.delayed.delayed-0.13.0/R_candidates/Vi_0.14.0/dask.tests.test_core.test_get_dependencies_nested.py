def test_get_dependencies_nested():
    dsk = {'x': 1, 'y': 2,
           'z': (add, (inc, [['x']]), 'y')}

    assert get_dependencies(dsk, 'z') == set(['x', 'y'])
    assert sorted(get_dependencies(dsk, 'z', as_list=True)) == ['x', 'y']
