def test_pseudodet_pinv():
    # Make sure that pseudo-inverse and pseudo-det agree on cutoff

    # Assemble random covariance matrix with large and small eigenvalues
    np.random.seed(1234)
    n = 7
    x = np.random.randn(n, n)
    cov = np.dot(x, x.T)
    s, u = scipy.linalg.eigh(cov)
    s = 0.5 * np.ones(n)
    s[0] = 1.0
    s[-1] = 1e-7
    cov = np.dot(u, np.dot(np.diag(s), u.T))

    # Set cond so that the lowest eigenvalue is below the cutoff
    cond = 1e-5
    psd = _PSD(cov, cond=cond)
    psd_pinv = _PSD(psd.pinv, cond=cond)

    # Check that the log pseudo-determinant agrees with the sum
    # of the logs of all but the smallest eigenvalue
    assert_allclose(psd.log_pdet, np.sum(np.log(s[:-1])))
    # Check that the pseudo-determinant of the pseudo-inverse
    # agrees with 1 / pseudo-determinant
    assert_allclose(-psd.log_pdet, psd_pinv.log_pdet)
