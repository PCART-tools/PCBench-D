def test_large_pseudo_determinant():
    # Check that large pseudo-determinants are handled appropriately.

    # Construct a singular diagonal covariance matrix
    # whose pseudo determinant overflows double precision.
    large_total_log = 1000.0
    npos = 100
    nzero = 2
    large_entry = np.exp(large_total_log / npos)
    n = npos + nzero
    cov = np.zeros((n, n), dtype=float)
    np.fill_diagonal(cov, large_entry)
    cov[-nzero:, -nzero:] = 0

    # Check some determinants.
    assert_equal(scipy.linalg.det(cov), 0)
    assert_equal(scipy.linalg.det(cov[:npos, :npos]), np.inf)

    # np.linalg.slogdet is only available in numpy 1.6+
    # but scipy currently supports numpy 1.5.1.
    # assert_allclose(np.linalg.slogdet(cov[:npos, :npos]),
    #                 (1, large_total_log))

    # Check the pseudo-determinant.
    psd = _PSD(cov)
    assert_allclose(psd.log_pdet, large_total_log)
