def test_regression_ticket_1326():
    # adjust to avoid nan with 0*log(0)
    assert_almost_equal(stats.chi2.pdf(0.0, 2), 0.5, 14)
