def test_tukeylambda_stats_ticket_1545():
    # Some test for the variance and kurtosis of the Tukey Lambda distr.
    # See test_tukeylamdba_stats.py for more tests.

    mv = stats.tukeylambda.stats(0, moments='mvsk')
    # Known exact values:
    expected = [0, np.pi**2/3, 0, 1.2]
    assert_almost_equal(mv, expected, decimal=10)

    mv = stats.tukeylambda.stats(3.13, moments='mvsk')
    # 'expected' computed with mpmath.
    expected = [0, 0.0269220858861465102, 0, -0.898062386219224104]
    assert_almost_equal(mv, expected, decimal=10)

    mv = stats.tukeylambda.stats(0.14, moments='mvsk')
    # 'expected' computed with mpmath.
    expected = [0, 2.11029702221450250, 0, -0.02708377353223019456]
    assert_almost_equal(mv, expected, decimal=10)
