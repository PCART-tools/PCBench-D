def test_gompertz_accuracy():
    # Regression test for gh-4031
    p = stats.gompertz.ppf(stats.gompertz.cdf(1e-100,1),1)
    assert_allclose(p, 1e-100)
