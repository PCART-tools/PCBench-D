def test_vonmises_line_support():
    assert_equal(stats.vonmises_line.a, -np.pi)
    assert_equal(stats.vonmises_line.b, np.pi)
