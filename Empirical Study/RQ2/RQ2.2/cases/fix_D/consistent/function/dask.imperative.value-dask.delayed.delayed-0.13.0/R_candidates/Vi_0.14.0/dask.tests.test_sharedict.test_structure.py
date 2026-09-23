def test_structure():
    s = ShareDict()
    s.update(a)
    s.update(b)
    s.update(c)

    assert all(any(d is x for d in s.dicts.values())
               for x in [a, b, c])
