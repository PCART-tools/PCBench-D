def test_slice_optimizations():
    #bar[:]
    expected = {('foo', 0): ('bar', 0)}
    result, chunks = slice_array('foo', 'bar', [[100]], (slice(None, None, None),))
    assert expected == result

    #bar[:,:,:]
    expected = {('foo', 0): ('bar', 0),
                ('foo', 1): ('bar', 1),
                ('foo', 2): ('bar', 2)}
    result, chunks = slice_array('foo', 'bar', [(100, 1000, 10000)],
                                 (slice(None, None, None),
                                  slice(None, None, None),
                                  slice(None, None, None)))
    assert expected == result
