def test_degenerate_distributions():
    for n in range(1, 5):
        x = np.random.randn(n)
        for k in range(1, n + 1):
            # Sample a small covariance matrix.
            s = np.random.randn(k, k)
            cov_kk = np.dot(s, s.T)

            # Embed the small covariance matrix into a larger low rank matrix.
            cov_nn = np.zeros((n, n))
            cov_nn[:k, :k] = cov_kk

            # Define a rotation of the larger low rank matrix.
            u = _sample_orthonormal_matrix(n)
            cov_rr = np.dot(u, np.dot(cov_nn, u.T))
            y = np.dot(u, x)

            # Check some identities.
            distn_kk = multivariate_normal(np.zeros(k), cov_kk,
                                           allow_singular=True)
            distn_nn = multivariate_normal(np.zeros(n), cov_nn,
                                           allow_singular=True)
            distn_rr = multivariate_normal(np.zeros(n), cov_rr,
                                           allow_singular=True)
            assert_equal(distn_kk.cov_info.rank, k)
            assert_equal(distn_nn.cov_info.rank, k)
            assert_equal(distn_rr.cov_info.rank, k)
            pdf_kk = distn_kk.pdf(x[:k])
            pdf_nn = distn_nn.pdf(x)
            pdf_rr = distn_rr.pdf(y)
            assert_allclose(pdf_kk, pdf_nn)
            assert_allclose(pdf_kk, pdf_rr)
            logpdf_kk = distn_kk.logpdf(x[:k])
            logpdf_nn = distn_nn.logpdf(x)
            logpdf_rr = distn_rr.logpdf(y)
            assert_allclose(logpdf_kk, logpdf_nn)
            assert_allclose(logpdf_kk, logpdf_rr)
