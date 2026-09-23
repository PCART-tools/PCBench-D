def test_wilcoxon_bad_arg():
    """Raise ValueError when two args of different lengths are given or
       zero_method is unknwon"""
    assert_raises(ValueError, stats.wilcoxon, [1], [1,2])
    assert_raises(ValueError, stats.wilcoxon, [1,2], [1,2], "dummy")
