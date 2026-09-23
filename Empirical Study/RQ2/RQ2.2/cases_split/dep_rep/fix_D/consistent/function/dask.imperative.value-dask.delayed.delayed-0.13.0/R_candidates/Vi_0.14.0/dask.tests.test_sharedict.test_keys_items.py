def test_keys_items():
    s = ShareDict()
    s.update_with_key(a, key='a')
    s.update_with_key(b, key='b')
    s.update_with_key(c, key='c')

    d = merge(a, b, c)

    for fn in [dict, set, len]:
        assert fn(s) == fn(d)

    for fn in [lambda x: x.values(), lambda x: x.keys(), lambda x: x.items()]:
        assert set(fn(s)) == set(fn(d))
