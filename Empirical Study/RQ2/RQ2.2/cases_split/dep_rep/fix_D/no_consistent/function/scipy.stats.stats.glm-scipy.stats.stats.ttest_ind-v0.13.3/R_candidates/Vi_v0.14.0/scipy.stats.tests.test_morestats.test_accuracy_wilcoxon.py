def test_accuracy_wilcoxon():
    freq = [1, 4, 16, 15, 8, 4, 5, 1, 2]
    nums = range(-4, 5)
    x = np.concatenate([[u] * v for u, v in zip(nums, freq)])
    y = np.zeros(x.size)

    T, p = stats.wilcoxon(x, y, "pratt")
    assert_allclose(T, 423)
    assert_allclose(p, 0.00197547303533107)

    T, p = stats.wilcoxon(x, y, "zsplit")
    assert_allclose(T, 441)
    assert_allclose(p, 0.0032145343172473055)

    T, p = stats.wilcoxon(x, y, "wilcox")
    assert_allclose(T, 327)
    assert_allclose(p, 0.00641346115861)

    # Test the 'correction' option, using values computed in R with:
    # > wilcox.test(x, y, paired=TRUE, exact=FALSE, correct={FALSE,TRUE})
    x = np.array([120, 114, 181, 188, 180, 146, 121, 191, 132, 113, 127, 112])
    y = np.array([133, 143, 119, 189, 112, 199, 198, 113, 115, 121, 142, 187])
    T, p = stats.wilcoxon(x, y, correction=False)
    assert_equal(T, 34)
    assert_allclose(p, 0.6948866, rtol=1e-6)
    T, p = stats.wilcoxon(x, y, correction=True)
    assert_equal(T, 34)
    assert_allclose(p, 0.7240817, rtol=1e-6)
