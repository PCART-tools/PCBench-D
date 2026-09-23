def test_boxcox_bad_arg():
    """Raise ValueError if any data value is negative."""
    x = np.array([-1])
    assert_raises(ValueError, stats.boxcox, x)
