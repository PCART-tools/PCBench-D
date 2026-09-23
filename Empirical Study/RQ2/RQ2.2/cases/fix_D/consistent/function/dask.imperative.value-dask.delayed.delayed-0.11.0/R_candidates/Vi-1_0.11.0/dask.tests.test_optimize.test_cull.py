def test_cull():
    # 'out' depends on 'x' and 'y', but not 'z'
    d = {'x': 1, 'y': (inc, 'x'), 'z': (inc, 'x'), 'out': (add, 'y', 10)}
    culled, dependencies = cull(d, 'out')
    assert culled == {'x': 1, 'y': (inc, 'x'), 'out': (add, 'y', 10)}
    assert dependencies == {'x': [], 'y': ['x'], 'out': ['y']}

    assert cull(d, 'out') == cull(d, ['out'])
    assert cull(d, ['out', 'z'])[0] == d
    assert cull(d, [['out'], ['z']]) == cull(d, ['out', 'z'])
    assert raises(KeyError, lambda: cull(d, 'badkey'))
