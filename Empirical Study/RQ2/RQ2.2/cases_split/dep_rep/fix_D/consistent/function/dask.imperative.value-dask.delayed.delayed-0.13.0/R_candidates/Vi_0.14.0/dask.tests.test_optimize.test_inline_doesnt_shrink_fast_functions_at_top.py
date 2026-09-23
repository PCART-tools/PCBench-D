def test_inline_doesnt_shrink_fast_functions_at_top():
    dsk = {'x': (inc, 'y'), 'y': 1}
    result = inline_functions(dsk, [], fast_functions=set([inc]))
    assert result == dsk
