def test_exception_nonsquare_cov():
    cov = [[1, 2, 3], [4, 5, 6]]
    assert_raises(ValueError, _psd_pinv_decomposed_log_pdet, cov)
