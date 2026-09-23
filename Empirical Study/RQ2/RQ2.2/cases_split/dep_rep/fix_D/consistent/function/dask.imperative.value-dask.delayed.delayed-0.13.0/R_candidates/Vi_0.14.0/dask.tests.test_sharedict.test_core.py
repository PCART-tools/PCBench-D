def test_core():
    s = ShareDict()
    assert isinstance(s, Mapping)

    s.update(a)
    s.update(b)

    assert s['x'] == 1
    with pytest.raises(KeyError):
        s['abc']

    with pytest.raises((NotImplementedError, TypeError)):
        s['abc'] = 123
