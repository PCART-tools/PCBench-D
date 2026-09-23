def test_exceptions_rise_to_top():
    dsk = {'x': 1, 'y': (bad, 'x')}
    assert raises(ValueError, lambda: get(dsk, 'y'))
