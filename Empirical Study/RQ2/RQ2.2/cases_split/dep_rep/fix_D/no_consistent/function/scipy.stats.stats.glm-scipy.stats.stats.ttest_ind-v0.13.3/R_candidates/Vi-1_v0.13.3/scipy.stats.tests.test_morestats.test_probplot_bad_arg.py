def test_probplot_bad_arg():
    """Raise ValueError when given an invalid distribution."""
    data = [1]
    assert_raises(ValueError, stats.probplot, data, dist="plate_of_shrimp")
