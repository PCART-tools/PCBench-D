def test_break_ties_by_str():
    dsk = {('x', i): (inc, i) for i in range(10)}
    x_keys = sorted(dsk)
    dsk['y'] = list(x_keys)

    o = order(dsk)
    expected = {'y': 0}
    expected.update({k: i + 1 for i, k in enumerate(x_keys)})

    assert o == expected
