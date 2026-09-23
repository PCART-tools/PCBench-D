def test_mvsdist_bad_arg():
    """Raise ValueError if fewer than two data points are given."""
    data = [1]
    assert_raises(ValueError, stats.mvsdist, data)
