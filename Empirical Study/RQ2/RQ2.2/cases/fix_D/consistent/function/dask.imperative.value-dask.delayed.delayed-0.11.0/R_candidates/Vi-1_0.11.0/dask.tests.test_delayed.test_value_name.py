def test_value_name():
    assert delayed(1)._key.startswith('int-')
    assert delayed(1, pure=True)._key.startswith('int-')
