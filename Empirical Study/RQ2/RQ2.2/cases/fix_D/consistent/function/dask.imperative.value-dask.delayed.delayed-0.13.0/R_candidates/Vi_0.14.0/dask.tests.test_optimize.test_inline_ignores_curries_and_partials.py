def test_inline_ignores_curries_and_partials():
    dsk = {'x': 1, 'y': 2,
           'a': (partial(add, 1), 'x'),
           'b': (inc, 'a')}

    result = inline_functions(dsk, [], fast_functions=set([add]))
    assert result['b'] == (inc, dsk['a'])
    assert 'a' not in result
