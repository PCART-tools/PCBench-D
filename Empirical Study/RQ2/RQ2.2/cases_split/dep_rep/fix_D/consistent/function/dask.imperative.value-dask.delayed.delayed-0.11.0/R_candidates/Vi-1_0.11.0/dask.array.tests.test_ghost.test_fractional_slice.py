def test_fractional_slice():
    assert fractional_slice(('x', 4.9), {0: 2}) == \
            (getitem, ('x', 5), (slice(0, 2),))

    assert fractional_slice(('x', 3, 5.1), {0: 2, 1: 3}) == \
            (getitem, ('x', 3, 5), (slice(None, None, None), slice(-3, None)))

    assert fractional_slice(('x', 2.9, 5.1), {0: 2, 1: 3}) == \
            (getitem, ('x', 3, 5), (slice(0, 2), slice(-3, None)))
