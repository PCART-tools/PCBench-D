def test_nan_is_sorted():
    line = mlines.Line2D([], [])
    assert line._is_sorted(np.array([1, 2, 3]))
    assert line._is_sorted(np.array([1, np.nan, 3]))
    assert not line._is_sorted([3, 5] + [np.nan] * 100 + [0, 2])
