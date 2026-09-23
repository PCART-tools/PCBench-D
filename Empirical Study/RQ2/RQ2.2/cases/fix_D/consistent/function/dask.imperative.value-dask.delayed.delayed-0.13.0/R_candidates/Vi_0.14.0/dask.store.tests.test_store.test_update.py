def test_update():
    s = Store()

    dsk = {'x': 1, 'y': (inc, 'x')}
    s.update(dsk)

    assert s['y'] == 2

    pytest.raises(Exception, lambda: s.update({'x': 2}))
    # Test that it doesn't raise
    s.update({'x': 1})
