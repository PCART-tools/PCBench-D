def test_update_with_sharedict():
    s = ShareDict()
    s.update_with_key(a, key='a')
    s.update_with_key(b, key='b')
    s.update_with_key(c, key='c')

    d = {'z': 5}

    s2 = ShareDict()
    s2.update_with_key(a, key='a')
    s2.update_with_key(d, key='d')

    s.update(s2)

    assert s.dicts['a'] is s.dicts['a']
