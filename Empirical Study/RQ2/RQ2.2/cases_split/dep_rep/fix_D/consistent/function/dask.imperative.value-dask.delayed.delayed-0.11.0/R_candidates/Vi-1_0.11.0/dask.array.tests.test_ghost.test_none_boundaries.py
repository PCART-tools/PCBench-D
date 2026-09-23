def test_none_boundaries():
    x = da.from_array(np.arange(16).reshape(4, 4), chunks=(2, 2))
    exp = boundaries(x, 2, {0: 'none', 1: 33})
    res = np.array(
          [[33, 33,  0,  1,  2,  3, 33, 33],
           [33, 33,  4,  5,  6,  7, 33, 33],
           [33, 33,  8,  9, 10, 11, 33, 33],
           [33, 33, 12, 13, 14, 15, 33, 33]])
    assert eq(exp, res)
