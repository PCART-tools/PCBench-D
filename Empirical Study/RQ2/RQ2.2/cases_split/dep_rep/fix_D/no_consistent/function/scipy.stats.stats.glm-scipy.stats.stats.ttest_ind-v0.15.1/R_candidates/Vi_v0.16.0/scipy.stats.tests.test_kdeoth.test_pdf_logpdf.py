def test_pdf_logpdf():
    np.random.seed(1)
    n_basesample = 50
    xn = np.random.randn(n_basesample)

    # Default
    gkde = stats.gaussian_kde(xn)

    xs = np.linspace(-15, 12, 25)
    pdf = gkde.evaluate(xs)
    pdf2 = gkde.pdf(xs)
    assert_almost_equal(pdf, pdf2, decimal=12)

    logpdf = np.log(pdf)
    logpdf2 = gkde.logpdf(xs)
    assert_almost_equal(logpdf, logpdf2, decimal=12)
