def test_reduction_series_invalid_axis():
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 5, 6], 'b': [3, 2, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [7, 8, 9], 'b': [0, 0, 0]},
                                  index=[9, 9, 9])}
    ddf1 = dd.DataFrame(dsk, 'x', ['a', 'b'], [0, 4, 9, 9])
    pdf1 = ddf1.compute()

    for axis in [1, 'columns']:
        for s in [ddf1.a, pdf1.a]: # both must behave the same
            assert raises(ValueError, lambda: s.sum(axis=axis))
            assert raises(ValueError, lambda: s.min(axis=axis))
            assert raises(ValueError, lambda: s.max(axis=axis))
            # only count doesn't have axis keyword
            assert raises(TypeError, lambda: s.count(axis=axis))
            assert raises(ValueError, lambda: s.std(axis=axis))
            assert raises(ValueError, lambda: s.var(axis=axis))
            assert raises(ValueError, lambda: s.mean(axis=axis))
