def test_slice_array_1d():
    #x[24::2]
    expected = {('y', 0): (getitem, ('x', 0), (slice(24, 25, 2),)),
                ('y', 1): (getitem, ('x', 1), (slice(1, 25, 2),)),
                ('y', 2): (getitem, ('x', 2), (slice(0, 25, 2),)),
                ('y', 3): (getitem, ('x', 3), (slice(1, 25, 2),))}
    result, chunks = slice_array('y', 'x', [[25] * 4], [slice(24, None, 2)])

    assert expected == result

    #x[26::2]
    expected = {('y', 0): (getitem, ('x', 1), (slice(1, 25, 2),)),
                ('y', 1): (getitem, ('x', 2), (slice(0, 25, 2),)),
                ('y', 2): (getitem, ('x', 3), (slice(1, 25, 2),))}

    result, chunks = slice_array('y', 'x', [[25] * 4], [slice(26, None, 2)])
    assert expected == result

    #x[24::2]
    expected = {('y', 0): (getitem, ('x', 0), (slice(24, 25, 2),)),
                ('y', 1): (getitem, ('x', 1), (slice(1, 25, 2),)),
                ('y', 2): (getitem, ('x', 2), (slice(0, 25, 2),)),
                ('y', 3): (getitem, ('x', 3), (slice(1, 25, 2),))}
    result, chunks = slice_array('y', 'x', [(25, ) * 4], (slice(24, None, 2), ))

    assert expected == result

    #x[26::2]
    expected = {('y', 0): (getitem, ('x', 1), (slice(1, 25, 2),)),
                ('y', 1): (getitem, ('x', 2), (slice(0, 25, 2),)),
                ('y', 2): (getitem, ('x', 3), (slice(1, 25, 2),))}

    result, chunks = slice_array('y', 'x', [(25, ) * 4], (slice(26, None, 2), ))
    assert expected == result
