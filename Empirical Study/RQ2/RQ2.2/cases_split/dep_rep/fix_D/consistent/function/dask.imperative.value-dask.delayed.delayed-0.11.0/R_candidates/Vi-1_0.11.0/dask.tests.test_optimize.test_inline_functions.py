def test_inline_functions():
    x, y, i, d = 'xyid'
    dsk = {'out': (add, i, d),
           i: (inc, x),
           d: (double, y),
           x: 1, y: 1}

    result = inline_functions(dsk, [], fast_functions=set([inc]))
    expected = {'out': (add, (inc, x), d),
                d: (double, y),
                x: 1, y: 1}
    assert result == expected
