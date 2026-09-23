def test_chi2_contingency_g():
    c = np.array([[15, 60], [15, 90]])
    g, p, dof, e = chi2_contingency(c, lambda_='log-likelihood', correction=False)
    assert_allclose(g, 2*xlogy(c, c/e).sum())

    g, p, dof, e = chi2_contingency(c, lambda_='log-likelihood', correction=True)
    c_corr = c + np.array([[-0.5, 0.5], [0.5, -0.5]])
    assert_allclose(g, 2*xlogy(c_corr, c_corr/e).sum())

    c = np.array([[10, 12, 10], [12, 10, 10]])
    g, p, dof, e = chi2_contingency(c, lambda_='log-likelihood')
    assert_allclose(g, 2*xlogy(c, c/e).sum())
