def test_column_optimizations_with_bcolz_and_rewrite():
    try:
        import bcolz
    except ImportError:
        return
    bc = bcolz.ctable([[1, 2, 3], [10, 20, 30]], names=['a', 'b'])
    func = lambda x: x
    for cols in [None, 'abc', ['abc']]:
        dsk2 = merge(dict((('x', i),
                          (dataframe_from_ctable, bc, slice(0, 2), cols, {}))
                          for i in [1, 2, 3]),
                     dict((('y', i),
                          (getitem, ('x', i), (list, ['a', 'b'])))
                          for i in [1, 2, 3]))

        expected = dict((('y', i), (dataframe_from_ctable,
                                     bc, slice(0, 2), (list, ['a', 'b']), {}))
                          for i in [1, 2, 3])

        result = dd.optimize(dsk2, [('y', i) for i in [1, 2, 3]])
        assert result == expected
