def test_ppcc_max_bad_arg():
    """Raise ValueError when given an invalid distribution."""
    data = [1]
    assert_raises(ValueError, stats.ppcc_max, data, dist="plate_of_shrimp")
