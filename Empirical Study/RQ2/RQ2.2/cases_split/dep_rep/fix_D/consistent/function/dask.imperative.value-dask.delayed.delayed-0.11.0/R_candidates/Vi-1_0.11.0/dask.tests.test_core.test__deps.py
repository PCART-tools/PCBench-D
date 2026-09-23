def test__deps():
    dsk = {'x': 1, 'y': 2}

    assert _deps(dsk, ['x', 'y']) == ['x', 'y']
