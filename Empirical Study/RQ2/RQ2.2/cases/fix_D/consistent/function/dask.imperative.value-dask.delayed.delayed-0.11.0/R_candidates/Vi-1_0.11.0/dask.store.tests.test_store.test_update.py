def test_update():
    s = Store()

    dsk = {'x': 1, 'y': (inc, 'x')}
    s.update(dsk)

    assert s['y'] == 2

    assert raises(Exception, lambda: s.update({'x': 2}))
    assert not raises(Exception, lambda: s.update({'x': 1}))
