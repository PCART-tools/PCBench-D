def test_exception_nonfinite_cov():
    cov_nan = [[1, 0], [0, np.nan]]
    assert_raises(ValueError, _psd_pinv_decomposed_log_pdet, cov_nan)
    cov_inf = [[1, 0], [0, np.inf]]
    assert_raises(ValueError, _psd_pinv_decomposed_log_pdet, cov_inf)
