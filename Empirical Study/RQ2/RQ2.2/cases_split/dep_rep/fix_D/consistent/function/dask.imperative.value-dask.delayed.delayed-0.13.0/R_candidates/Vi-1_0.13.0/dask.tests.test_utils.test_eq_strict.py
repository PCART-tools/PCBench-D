def test_eq_strict():
    assert eq_strict('a', 'a')
    assert not eq_strict(b'a', u'a')
