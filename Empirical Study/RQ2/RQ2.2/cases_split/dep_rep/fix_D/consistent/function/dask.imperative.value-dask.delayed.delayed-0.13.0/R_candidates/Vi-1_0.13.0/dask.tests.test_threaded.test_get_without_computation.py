def test_get_without_computation():
    dsk = {'x': 1}
    assert get(dsk, 'x') == 1
