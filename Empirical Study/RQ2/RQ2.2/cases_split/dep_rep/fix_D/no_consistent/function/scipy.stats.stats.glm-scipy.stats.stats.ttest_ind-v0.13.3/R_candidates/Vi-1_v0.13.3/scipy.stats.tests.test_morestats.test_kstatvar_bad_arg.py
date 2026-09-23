def test_kstatvar_bad_arg():
    """Raise ValueError is n is not 1 or 2."""
    data = [1]
    n = 10
    assert_raises(ValueError, stats.kstatvar, data, n=n)
