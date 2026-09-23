def test_slice_1d():
    expected = {0: slice(10, 25, 1), 1: slice(None, None, None), 2: slice(0, 1, 1)}
    result = _slice_1d(100, [25]*4, slice(10, 51, None))
    assert expected == result

    #x[100:12:-3]
    expected = {0: slice(-2, -8, -3),
                1: slice(-1, -21, -3),
                2: slice(-3, -21, -3),
                3: slice(-2, -21, -3),
                4: slice(-1, -21, -3)}
    result = _slice_1d(100, [20]*5, slice(100, 12, -3))
    assert expected == result

    #x[102::-3]
    expected = {0: slice(-2, -21, -3),
                1: slice(-1, -21, -3),
                2: slice(-3, -21, -3),
                3: slice(-2, -21, -3),
                4: slice(-1, -21, -3)}
    result = _slice_1d(100, [20]*5, slice(102, None, -3))
    assert expected == result

    #x[::-4]
    expected = {0: slice(-1, -21, -4),
                1: slice(-1, -21, -4),
                2: slice(-1, -21, -4),
                3: slice(-1, -21, -4),
                4: slice(-1, -21, -4)}
    result = _slice_1d(100, [20]*5, slice(None, None, -4))
    assert expected == result

    #x[::-7]
    expected = {0: slice(-5, -21, -7),
                1: slice(-4, -21, -7),
                2: slice(-3, -21, -7),
                3: slice(-2, -21, -7),
                4: slice(-1, -21, -7)}
    result = _slice_1d(100, [20]*5, slice(None, None, -7))
    assert expected == result

    #x=range(115)
    #x[::-7]
    expected = {0: slice(-7, -24, -7),
                1: slice(-2, -24, -7),
                2: slice(-4, -24, -7),
                3: slice(-6, -24, -7),
                4: slice(-1, -24, -7)}
    result = _slice_1d(115, [23]*5, slice(None, None, -7))
    assert expected == result

    #x[79::-3]
    expected = {0: slice(-1, -21, -3),
                1: slice(-3, -21, -3),
                2: slice(-2, -21, -3),
                3: slice(-1, -21, -3)}
    result = _slice_1d(100, [20]*5, slice(79, None, -3))
    assert expected == result

    #x[-1:-8:-1]
    expected = {4: slice(-1, -8, -1)}
    result = _slice_1d(100, [20, 20, 20, 20, 20], slice(-1, 92, -1))
    assert expected == result

    #x[20:0:-1]
    expected = {0: slice(-1, -20, -1),
                1: slice(-20, -21, -1)}
    result = _slice_1d(100, [20, 20, 20, 20, 20], slice(20, 0, -1))
    assert expected == result

    #x[:0]
    expected = {}
    result = _slice_1d(100, [20, 20, 20, 20, 20], slice(0))
    assert result

    #x=range(99)
    expected = {0: slice(-3, -21, -3),
                1: slice(-2, -21, -3),
                2: slice(-1, -21, -3),
                3: slice(-2, -20, -3),
                4: slice(-1, -21, -3)}
    #This array has non-uniformly sized blocks
    result = _slice_1d(99, [20, 20, 20, 19, 20], slice(100, None, -3))
    assert expected == result

    #x=range(104)
    #x[::-3]
    expected = {0: slice(-1, -21, -3),
                1: slice(-3, -24, -3),
                2: slice(-3, -28, -3),
                3: slice(-1, -14, -3),
                4: slice(-1, -22, -3)}
    #This array has non-uniformly sized blocks
    result = _slice_1d(104, [20, 23, 27, 13, 21], slice(None, None, -3))
    assert expected == result

    #x=range(104)
    #x[:27:-3]
    expected = {1: slice(-3, -16, -3),
                2: slice(-3, -28, -3),
                3: slice(-1, -14, -3),
                4: slice(-1, -22, -3)}
    #This array has non-uniformly sized blocks
    result = _slice_1d(104, [20, 23, 27, 13, 21], slice(None, 27, -3))
    assert expected == result

    #x=range(104)
    #x[100:27:-3]
    expected = {1: slice(-3, -16, -3),
                2: slice(-3, -28, -3),
                3: slice(-1, -14, -3),
                4: slice(-4, -22, -3)}
    #This array has non-uniformly sized blocks
    result = _slice_1d(104, [20, 23, 27, 13, 21], slice(100, 27, -3))
    assert expected == result
