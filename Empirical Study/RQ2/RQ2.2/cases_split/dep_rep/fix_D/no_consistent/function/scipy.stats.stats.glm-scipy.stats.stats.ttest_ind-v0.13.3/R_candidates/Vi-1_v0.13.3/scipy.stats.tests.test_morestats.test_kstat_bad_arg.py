def test_kstat_bad_arg():
    """Raise ValueError if n > 4 or n > 1."""
    data = [1]
    n = 10
    assert_raises(ValueError, stats.kstat, data, n=n)
