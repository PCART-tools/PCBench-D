def test_inline_functions_protects_output_keys():
    dsk = {'x': (inc, 1), 'y': (double, 'x')}
    assert inline_functions(dsk, [], [inc]) == {'y': (double, (inc, 1))}
    assert inline_functions(dsk, ['x'], [inc]) == {'y': (double, 'x'),
                                                   'x': (inc, 1)}
