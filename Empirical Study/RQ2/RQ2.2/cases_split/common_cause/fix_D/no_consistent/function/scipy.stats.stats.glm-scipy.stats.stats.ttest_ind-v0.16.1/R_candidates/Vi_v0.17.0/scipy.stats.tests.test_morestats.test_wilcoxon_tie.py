def test_wilcoxon_tie():
    # Regression test for gh-2391.
    # Corresponding R code is:
    #   > result = wilcox.test(rep(0.1, 10), exact=FALSE, correct=FALSE)
    #   > result$p.value
    #   [1] 0.001565402
    #   > result = wilcox.test(rep(0.1, 10), exact=FALSE, correct=TRUE)
    #   > result$p.value
    #   [1] 0.001904195
    stat, p = stats.wilcoxon([0.1] * 10)
    expected_p = 0.001565402
    assert_equal(stat, 0)
    assert_allclose(p, expected_p, rtol=1e-6)

    stat, p = stats.wilcoxon([0.1] * 10, correction=True)
    expected_p = 0.001904195
    assert_equal(stat, 0)
    assert_allclose(p, expected_p, rtol=1e-6)
