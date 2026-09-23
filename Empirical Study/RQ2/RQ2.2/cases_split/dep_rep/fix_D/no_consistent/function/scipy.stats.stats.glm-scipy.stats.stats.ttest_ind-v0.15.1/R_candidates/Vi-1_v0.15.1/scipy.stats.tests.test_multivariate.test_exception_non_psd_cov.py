def test_exception_non_psd_cov():
    cov = [[1, 0], [0, -1]]
    assert_raises(ValueError, _PSD, cov)
